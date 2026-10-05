def set_author(self, board_id: str, author: str, allowed: bool):
    board = self._board(board_id)
    if board["owner"] != _address(gl.message.sender_address):
        raise gl.vm.UserError("Only the board owner may manage authors")
    normalized_author = _address(author)
    board["authors"][normalized_author] = bool(allowed)
