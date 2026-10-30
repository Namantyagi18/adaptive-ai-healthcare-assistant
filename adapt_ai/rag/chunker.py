"""Document chunking engine for medical text.

Preserves sentence boundaries and clinical context through sliding windows with overlap.
"""

import re
from typing import List, Dict, Any


class MedicalChunker:
    """Splits medical documents into semantically coherent passages with overlap."""

    def __init__(self, target_words: int = 150, overlap_words: int = 30):
        self.target_words = target_words
        self.overlap_words = overlap_words

    def split_into_sentences(self, text: str) -> List[str]:
        """Splits text along sentence boundaries while preserving medical abbreviations."""
        # Replace abbreviations temporarily with placeholders
        abbreviations = {
            "e.g.": "EG_PLACEHOLDER",
            "i.e.": "IE_PLACEHOLDER",
            "Dr.": "DR_PLACEHOLDER",
            "vs.": "VS_PLACEHOLDER",
            "dept.": "DEPT_PLACEHOLDER",
            "approx.": "APPROX_PLACEHOLDER"
        }
        processed = text
        for abbr, placeholder in abbreviations.items():
            processed = processed.replace(abbr, placeholder)

        # Split on sentence ending punctuation followed by space
        raw_sentences = re.split(r'(?<=[.!?])\s+', processed)

        sentences = []
        for s in raw_sentences:
            s_clean = s.strip()
            if not s_clean:
                continue
            # Restore abbreviations
            for abbr, placeholder in abbreviations.items():
                s_clean = s_clean.replace(placeholder, abbr)
            sentences.append(s_clean)

        return sentences

    def chunk_document(self, parsed_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunks a parsed medical document into indexed segments with provenance."""
        sentences = self.split_into_sentences(parsed_doc["content"])
        chunks = []
        current_chunk_words: List[str] = []
        current_sentences: List[str] = []
        chunk_index = 0

        for sentence in sentences:
            sentence_words = sentence.split()
            if len(current_chunk_words) + len(sentence_words) > self.target_words and current_sentences:
                # Flush current chunk
                chunk_text = " ".join(current_sentences)
                chunk_id = f"{parsed_doc['doc_id']}_chk{chunk_index}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "doc_id": parsed_doc["doc_id"],
                    "chunk_index": chunk_index,
                    "title": parsed_doc["title"],
                    "source": parsed_doc["source"],
                    "category": parsed_doc["category"],
                    "text": chunk_text,
                    "word_count": len(current_chunk_words)
                })
                chunk_index += 1

                # Retain overlap sentences
                overlap_word_count = 0
                retained_sentences = []
                for s in reversed(current_sentences):
                    words = s.split()
                    if overlap_word_count + len(words) <= self.overlap_words:
                        retained_sentences.insert(0, s)
                        overlap_word_count += len(words)
                    else:
                        break
                
                current_sentences = retained_sentences + [sentence]
                current_chunk_words = [w for s in current_sentences for w in s.split()]
            else:
                current_sentences.append(sentence)
                current_chunk_words.extend(sentence_words)

        # Flush final remainder
        if current_sentences:
            chunk_text = " ".join(current_sentences)
            chunk_id = f"{parsed_doc['doc_id']}_chk{chunk_index}"
            chunks.append({
                "chunk_id": chunk_id,
                "doc_id": parsed_doc["doc_id"],
                "chunk_index": chunk_index,
                "title": parsed_doc["title"],
                "source": parsed_doc["source"],
                "category": parsed_doc["category"],
                "text": chunk_text,
                "word_count": len(current_chunk_words)
            })

        return chunks
