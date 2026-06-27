"""Command-line interface for Gomoku (五子棋)."""

from .game import Board, Player, BOARD_SIZE


def _parse_coord(raw: str) -> tuple[int, int] | None:
    """Try to parse a coordinate like ``3 7``.  Returns ``None`` on failure."""
    parts = raw.strip().split()
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def main() -> None:
    """Run an interactive Gomoku game."""
    board = Board()
    current_player = Player.BLACK

    print("=== 五子棋 (Gomoku) ===")
    print("Enter coordinates as:  x y")
    print("Valid range: 0 — 14 for both axes.")
    print("Type 'q' to quit.\n")
    print(board.display())

    while True:
        try:
            raw = input(f"\n{current_player.value} Player's turn (x y): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if raw.lower() in ("q", "quit", "exit"):
            print("Game abandoned.")
            break

        coord = _parse_coord(raw)
        if coord is None:
            print("Invalid input.  Use the format:  x y  (e.g. 7 7)")
            continue

        x, y = coord

        if not Board.is_on_board(x, y):
            print(
                f"({x}, {y}) is out of bounds. "
                f"Valid range: 0 – {BOARD_SIZE - 1}"
            )
            continue

        if not board.is_empty(x, y):
            print(f"Cell ({x}, {y}) is already taken.  Choose another.")
            continue

        board.place(x, y, current_player)
        print()
        print(board.display())

        if board.check_win(x, y, current_player):
            print(f"\n{current_player.value} Player wins! 🎉")
            break

        if board.is_full():
            print("\nIt's a draw! The board is full.")
            break

        current_player = current_player.opponent


if __name__ == "__main__":
    main()
