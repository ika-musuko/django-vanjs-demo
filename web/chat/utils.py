def chunker(sequence, size):
    """Yields successive size-sized chunks from a sequence."""
    for pos in range(0, len(sequence), size):
        yield sequence[pos:pos + size]
