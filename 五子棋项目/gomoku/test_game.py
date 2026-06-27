"""Tests for the Gomoku game logic."""

import pytest

from gomoku.game import Board, Player, BOARD_SIZE


# ======================================================================
# Fixtures
# ======================================================================


@pytest.fixture
def board() -> Board:
    return Board()


# ======================================================================
# Player enum
# ======================================================================


class TestPlayer:
    def test_opponent(self) -> None:
        assert Player.BLACK.opponent is Player.WHITE
        assert Player.WHITE.opponent is Player.BLACK


# ======================================================================
# Board initialisation
# ======================================================================


class TestBoardInit:
    def test_all_cells_empty(self, board: Board) -> None:
        """A fresh board has no stones anywhere."""
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                assert board.is_empty(x, y), f"({x}, {y}) should be empty"

    def test_no_winner_on_empty_board(self, board: Board) -> None:
        """No win on a fresh board (place a stone and check around it)."""
        board.place(7, 7, Player.BLACK)
        assert not board.check_win(7, 7, Player.BLACK)

    def test_board_not_full(self, board: Board) -> None:
        assert not board.is_full()

    def test_is_empty_out_of_bounds(self, board: Board) -> None:
        """is_empty returns False for coordinates off the board."""
        assert not board.is_empty(-1, 0)
        assert not board.is_empty(0, -1)
        assert not board.is_empty(15, 0)
        assert not board.is_empty(0, 15)

    def test_grid_is_readonly(self, board: Board) -> None:
        """The grid property should not be modifiable, even at non-symmetric indices."""
        grid = board.grid
        with pytest.raises(TypeError):
            grid[0][0] = Player.BLACK  # type: ignore[index]
        with pytest.raises(TypeError):
            grid[7][3] = Player.WHITE  # type: ignore[index]

    def test_display_format(self, board: Board) -> None:
        """display() produces column headers, row labels, and uses · for empty."""
        output = board.display()
        lines = output.splitlines()
        # Header line starts with spaces then column numbers
        assert lines[0].startswith("   ")
        assert "0" in lines[0] and "14" in lines[0]
        # First data line starts with row label
        assert lines[1].lstrip().startswith("0")
        # Empty cells show as ·
        assert "·" in output


# ======================================================================
# Place moves
# ======================================================================


class TestPlace:
    def test_place_valid(self, board: Board) -> None:
        board.place(0, 0, Player.BLACK)
        assert board.grid[0][0] is Player.BLACK

    def test_place_out_of_bounds_negative(self, board: Board) -> None:
        with pytest.raises(ValueError, match="out of bounds"):
            board.place(-1, 5, Player.BLACK)

    def test_place_out_of_bounds_too_large(self, board: Board) -> None:
        with pytest.raises(ValueError, match="out of bounds"):
            board.place(15, 5, Player.BLACK)

    def test_place_on_occupied_cell(self, board: Board) -> None:
        board.place(7, 7, Player.BLACK)
        with pytest.raises(ValueError, match="already occupied"):
            board.place(7, 7, Player.WHITE)

    def test_is_on_board_static(self) -> None:
        assert Board.is_on_board(0, 0)
        assert Board.is_on_board(14, 14)
        assert not Board.is_on_board(-1, 0)
        assert not Board.is_on_board(0, 15)


# ======================================================================
# Win detection – horizontal, vertical, diagonal
# ======================================================================


class TestWinDetection:
    """Test every direction with exactly five consecutive stones."""

    # --- Horizontal ---------------------------------------------------

    def test_horizontal_win(self, board: Board) -> None:
        """Five in a row → win."""
        line = [(3, 5), (4, 5), (5, 5), (6, 5), (7, 5)]
        for i, (x, y) in enumerate(line):
            board.place(x, y, Player.BLACK)
            # Only the last stone creates the five
            if i == 4:
                assert board.check_win(x, y, Player.BLACK)
            else:
                assert not board.check_win(x, y, Player.BLACK)

    def test_isolated_stone_not_win(self, board: Board) -> None:
        """A stone placed far from others is not a win (regardless of count nearby)."""
        for x in range(4):
            board.place(x, 0, Player.BLACK)
        # Place a separate stone that also isn't a winning move
        board.place(10, 0, Player.BLACK)
        assert not board.check_win(10, 0, Player.BLACK)

    def test_horizontal_six_stones_still_win(self, board: Board) -> None:
        """Six consecutive stones still count as a win (≥5)."""
        for x in range(6):
            board.place(x, 0, Player.BLACK)
        assert board.check_win(5, 0, Player.BLACK)

    # --- Vertical -----------------------------------------------------

    def test_vertical_win(self, board: Board) -> None:
        """Five in a column → win."""
        line = [(4, 2), (4, 3), (4, 4), (4, 5), (4, 6)]
        for i, (x, y) in enumerate(line):
            board.place(x, y, Player.WHITE)
            if i == 4:
                assert board.check_win(x, y, Player.WHITE)
            else:
                assert not board.check_win(x, y, Player.WHITE)

    # --- Diagonal ↘ ---------------------------------------------------

    def test_diagonal_down_right_win(self, board: Board) -> None:
        """Five stones on a ↘ diagonal → win."""
        line = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
        for i, (x, y) in enumerate(line):
            board.place(x, y, Player.BLACK)
            if i == 4:
                assert board.check_win(x, y, Player.BLACK)
            else:
                assert not board.check_win(x, y, Player.BLACK)

    # --- Diagonal ↗ ---------------------------------------------------

    def test_diagonal_up_right_win(self, board: Board) -> None:
        """Five stones on a ↗ diagonal → win."""
        line = [(2, 6), (3, 5), (4, 4), (5, 3), (6, 2)]
        for i, (x, y) in enumerate(line):
            board.place(x, y, Player.WHITE)
            if i == 4:
                assert board.check_win(x, y, Player.WHITE)
            else:
                assert not board.check_win(x, y, Player.WHITE)

    # --- Edge-boundary wins -------------------------------------------

    def test_horizontal_win_on_right_edge(self, board: Board) -> None:
        """Five in a row flush against the right edge (x=10…14)."""
        for x in range(10, 15):
            board.place(x, 14, Player.BLACK)
        assert board.check_win(14, 14, Player.BLACK)

    def test_horizontal_win_on_left_edge(self, board: Board) -> None:
        """Five in a row flush against the left edge (x=0…4)."""
        for x in range(5):
            board.place(x, 0, Player.BLACK)
        assert board.check_win(4, 0, Player.BLACK)

    def test_vertical_win_on_top_edge(self, board: Board) -> None:
        """Five in a column flush against the top edge (y=0…4)."""
        for y in range(5):
            board.place(0, y, Player.BLACK)
        assert board.check_win(0, 4, Player.BLACK)

    def test_vertical_win_on_bottom_edge(self, board: Board) -> None:
        """Five in a column flush against the bottom edge (y=10…14)."""
        for y in range(10, 15):
            board.place(14, y, Player.BLACK)
        assert board.check_win(14, 14, Player.BLACK)

    # --- Non-winning edge cases ---------------------------------------

    def test_opponent_stone_breaks_streak(self, board: Board) -> None:
        """Black · · · · Black with a White in the middle → no win for
        either after the 5th black stone."""
        positions = [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9)]
        for x, y in positions[:2]:
            board.place(x, y, Player.BLACK)
        board.place(5, 7, Player.WHITE)  # opponent breaks
        board.place(5, 8, Player.BLACK)
        board.place(5, 9, Player.BLACK)
        assert not board.check_win(5, 9, Player.BLACK)

    def test_win_only_for_current_player(self, board: Board) -> None:
        """Black makes five but check with WHITE → no win."""
        for x in range(5):
            board.place(x, 0, Player.BLACK)
        # Check from white's perspective
        assert not board.check_win(4, 0, Player.WHITE)

    def test_no_win_at_empty_cell_near_five(self, board: Board) -> None:
        """check_win at an empty cell next to five in a row → no win."""
        for x in range(5):
            board.place(x, 0, Player.BLACK)
        assert not board.check_win(5, 0, Player.BLACK)

    def test_no_win_at_opponent_cell_near_five(self, board: Board) -> None:
        """check_win at an opponent's cell next to five in a row → no win."""
        for x in range(5):
            board.place(x, 0, Player.BLACK)
        board.place(5, 0, Player.WHITE)
        assert not board.check_win(5, 0, Player.BLACK)


# ======================================================================
# Draw
# ======================================================================


class TestDraw:
    def test_is_full_detection(self, board: Board) -> None:
        """Fill every cell and verify is_full returns True."""
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                player = Player.BLACK if (x + y) % 2 == 0 else Player.WHITE
                board.place(x, y, player)
        assert board.is_full()

    def test_is_full_not_full(self, board: Board) -> None:
        """A board with one empty cell is not full."""
        # Fill all but one cell
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if x == 14 and y == 14:
                    continue
                player = Player.BLACK if (x + y) % 2 == 0 else Player.WHITE
                board.place(x, y, player)
        assert not board.is_full()


# ======================================================================
# CLI helpers
# ======================================================================


class TestCli:
    """Tests for the CLI module's helper functions."""

    def test_parse_coord_valid(self) -> None:
        from gomoku.cli import _parse_coord

        assert _parse_coord("3 7") == (3, 7)
        assert _parse_coord("0 14") == (0, 14)
        assert _parse_coord("  10  5  ") == (10, 5)

    def test_parse_coord_invalid(self) -> None:
        from gomoku.cli import _parse_coord

        assert _parse_coord("") is None
        assert _parse_coord("abc") is None
        assert _parse_coord("3") is None
        assert _parse_coord("3 7 9") is None
        assert _parse_coord("x y") is None
