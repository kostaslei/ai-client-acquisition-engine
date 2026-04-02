def select_top_chunks(ranked, max_chars):
    total_chars = 0
    selected = []

    for chunk, _ in ranked:
        if total_chars + len(chunk) > max_chars:
            break

        selected.append(chunk)
        total_chars += len(chunk)

    return selected