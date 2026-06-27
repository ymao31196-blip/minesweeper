"""Core game logic for Gomoku (五子棋)."""

from __future__ import annotations

from enum import Enum
from typing import Optional

BOARD_SIZE = 15


class Player(str, Enum):
    """Represents a player's stone on the board."""

    BLACK = "●"
    WHITE = "○"

    @property
    def opponent(self) -> Player:
        return Player.WHITE if self is Player.BLACK else Player.BLACK


class Board:
    """A 15×15 Gomoku board.

    The board is stored as a list of lists.  Each cell is ``None`` (empty)
    or a :class:`Player` value.
    """

    def __init__(self) -> None:
        self._grid: list[list[Optional[Player]]] = [
            [None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]

    @property
    def grid(self) -> tuple[tuple[Optional[Player], ...], ...]:
        """Read-only view of the board as a tuple of tuples."""
        return tuple(tuple(row) for row in self._grid)

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    @staticmethod
    def is_on_board(x: int, y: int) -> bool:
        """Return ``True`` if (x, y) is a valid board coordinate."""
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

    def is_empty(self, x: int, y: int) -> bool:
        """Return ``True`` if the cell at (x, y) is empty and on the board."""
        if not self.is_on_board(x, y):
            return False
        return self._grid[y][x] is None

    # ------------------------------------------------------------------
    # Core actions
    # ------------------------------------------------------------------

    def place(self, x: int, y: int, player: Player) -> None:
        """Place *player*'s stone at (x, y).

        Raises :class:`ValueError` if the coordinate is invalid or the
        cell is already occupied.
        """
        if not self.is_on_board(x, y):
            raise ValueError(
                f"({x}, {y}) is out of bounds. "
                f"Valid range: 0–{BOARD_SIZE - 1}"
            )
        if not self.is_empty(x, y):
            raise ValueError(
                f"Cell ({x}, {y}) is already occupied."
            )
        self._grid[y][x] = player

    def check_win(self, x: int, y: int, player: Player) -> bool:
        """Check whether the last move at (x, y) created a five-in-a-row.

        Must be called *after* :meth:`place`.
        """
        # Guard: the cell must actually belong to *player*
        if not self.is_on_board(x, y) or self._grid[y][x] is not player:
            return False

        # Four direction vectors: →  ↓  ↘  ↙
        directions = [
            (1, 0),   # horizontal
            (0, 1),   # vertical
            (1, 1),   # diagonal ↘
            (1, -1),  # diagonal ↗
        ]

        for dx, dy in directions:
            count = 1  # the stone just placed

            # Count in the positive direction
            nx, ny = x + dx, y + dy
            while (
                self.is_on_board(nx, ny)
                and self._grid[ny][nx] is player
            ):
                count += 1
                nx += dx
                ny += dy

            # Count in the negative direction
            nx, ny = x - dx, y - dy
            while (
                self.is_on_board(nx, ny)
                and self._grid[ny][nx] is player
            ):
                count += 1
                nx -= dx
                ny -= dy

            if count >= 5:
                return True

        return False

    def is_full(self) -> bool:
        """Return ``True`` if every cell is occupied."""
        return all(
            self._grid[y][x] is not None
            for y in range(BOARD_SIZE)
            for x in range(BOARD_SIZE)
        )

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def display(self) -> str:
        """Return a human-readable string representation of the board."""
        # Column header
        header = "   " + " ".join(f"{i:2d}" for i in range(BOARD_SIZE))
        lines = [header]

        for y in range(BOARD_SIZE):
            row_parts = [f"{y:2d} "]
            for x in range(BOARD_SIZE):
                cell = self._grid[y][x]
                if cell is Player.BLACK:
                    row_parts.append(" ●")
                elif cell is Player.WHITE:
                    row_parts.append(" ○")
                else:
                    row_parts.append(" ·")
            lines.append("".join(row_parts))

        return "\n".join(lines)

    def __str__(self) -> str:
        return self.display()
