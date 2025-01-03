'''Creates a class for Human backgammon pieces
Created 2024
@author: Anni Ainesaz and Shira Bartal
'''
import random
import copy

class Human_Player:
    def __init__(self, color):
        self.color = color
        if self.color == "black":
            self._pieces = [6, 6, 6, 6, 6,
                            8, 8, 8,
                            13, 13, 13, 13, 13,
                            24, 24]
        else:
            self._pieces = [1, 1,
                            12, 12, 12, 12, 12,
                            17, 17, 17,
                            19, 19, 19, 19, 19]

    def get_pieces(self):
        return self._pieces

    def set_pieces(self, list_of_pieces):
        self._pieces = list_of_pieces
        self.order()

    def get_other_pieces(self):
        return self.other_pieces

    def move_piece(self, distance, piece, other, r):  # piece is where to move from
        if self.color == "white":
            if distance <= 0:
                raise ValueError('Distance must be greater than 0')
            if piece != 0 and self.capturedPiece():
                raise ValueError('You must move your captured piece first')
            if piece in self._pieces:
                idx = self._pieces.index(piece)
                if self.validMove(piece, piece + distance, other, r):
                    self._pieces[idx] = piece + distance
                else:
                    raise ValueError('That is an invalid place to move your piece')
            else:
                raise ValueError('The chosen piece is not valid')
            self.capture(other)
            self.order()
        else:
            if distance <= 0:
                raise ValueError('Distance must be greater than 0')
            if piece != 25 and self.capturedPiece():
                raise ValueError('You must move your captured piece first')
            if piece in self._pieces:
                idx = self._pieces.index(piece)
                if self.validMove(piece, piece - distance, other, r):
                    self._pieces[idx] = piece - distance
                else:
                    raise ValueError('That is an invalid place to move your piece')
            else:
                raise ValueError('The chosen piece is not valid')
            self.capture(other)
            self.order()

    def __str__(self):
        return 'Your pieces are at: ' + str(self._pieces)

    def order(self):
        self._pieces.sort()

    def capturedPiece(self):# checks if I was eaten
        if self.color == "white":
            if 0 in self._pieces:
                return True
            else:
                return False
        else:
            if 25 in self._pieces:
                return True
            else:
                return False

    def capture(self, other):  # I eat
        if self.color == "white":
            op = other.get_pieces()[:]
            for piece in self._pieces:
                if piece in op:
                    op[op.index(piece)] = 25
            other.set_pieces(op)
        else:
            op = other.get_pieces()[:]
            for piece in self._pieces:
                if piece in op:
                    op[op.index(piece)] = 0
            other.set_pieces(op)


    def validMove(self, makor, yaad, other, r):
        idx = [i for i, x in enumerate(other.get_pieces()) if (x == yaad and x != 0 and x != 25)]
        no_oponent = len(idx) <= 1  # the oponent has max 1 pieces in yaad

        if str(yaad - makor) in r and 1 <= int(yaad) <= 24:
            return no_oponent

        elif self.color == "white" and yaad >= 25:  # the player wants to get piece out of home
            can_out = self._pieces[0] >= 19  # checks that all pieces in home
            if str(abs(yaad - makor)) not in r:
                relevant_roll = [x for x in r if int(yaad - makor) <= int(x)]
                if relevant_roll:
                    distance = min(relevant_roll)
                    # all pieces at home and there are no pieces between
                    pieces_between = [x for x in self._pieces if (25 - int(distance) <= x < int(makor))]
                    can_out = can_out and (not pieces_between)
            return can_out

        elif self.color == "black" and yaad <= 0:  # the player wants to get piece out of home
            can_out = all(x <= 6 for x in self._pieces)  # checks that all pieces in home
            if str(makor) not in r:
                relevant_roll = [x for x in r if makor <= int(x)]
                if relevant_roll:
                    distance = min(relevant_roll)
                    # all pieces at home and there are no pieces between
                    pieces_between = [x for x in self._pieces if (int(makor) < x <= int(distance))]
                    can_out = can_out and (not pieces_between)
            return can_out

        return no_oponent

    def win(self):
        if (self.color == "black" and all(piece == 0 for piece in self._pieces)) or (
                self.color == "white" and all(piece == 25 for piece in self._pieces)):
            return True
        else:
            return False

    def lose(self):
        if (self.color == "black" and all(piece == 25 for piece in self.other_pieces)) or (
                self.color == "white" and all(piece == 0 for piece in self.other_pieces)):
            return True
        else:
            return False


    #-----------------------------------------Random Option---------------------------

    def move_piece_random(self, distance, piece):  # piece is where to move from
        if distance <= 0:
            raise ValueError('Distance must be greater than 0')
        if ((self.color == "black" and piece != 25) or (self.color == "white" and piece != 0)) and self.capturedPieceRandom():
            raise ValueError('You must move your captured piece first')
        if piece in self._pieces:
            idx = self._pieces.index(piece)
            if self.color == "black":
                self._pieces[idx] = piece - distance

            elif self.color == "white":
                self._pieces[idx] = piece + distance
            else:
                raise ValueError('That is an invalid place to move your piece')
        else:
            raise ValueError('The chosen piece is not valid')
        self.captureRandom()
        self.order()

    def capturedPieceRandom(self):
        if ((self.color == "black") and (25 in self._pieces)) or ((self.color == "white") and (0 in self._pieces)):
            return True
        else:
            return False

    def captureRandom(self):
        op = self.other_pieces[:]
        for piece in self._pieces:
            if piece in op:
                if self.color == "black":
                    op[op.index(piece)] = 0
                elif self.color == "white":
                    op[op.index(piece)] = 25
        self.other_pieces = sorted(op)[:]

    def validMoveRandom(self, makor, yaad, r, my_pieces, other_pieces):
        idx = [i for i, x in enumerate(other_pieces) if (x == yaad and x != 0 and x != 25)]
        no_oponent = len(idx) <= 1  # the oponent has max 1 pieces in yaad

        if str(yaad - makor) in r and 1 <= int(yaad) <= 24:
            return no_oponent

        elif self.color == "white" and yaad >= 25:  # the player wants to get piece out of home
            can_out = my_pieces[0] >= 19  # checks that all pieces in home
            if str(abs(yaad - makor)) not in r:
                relevant_roll = [x for x in r if int(yaad - makor) <= int(x)]
                if relevant_roll:
                    distance = min(relevant_roll)
                    # all pieces at home and there are no pieces between
                    pieces_between = [x for x in my_pieces if (25 - int(distance) <= x < int(makor))]
                    can_out = can_out and (not pieces_between)
            return can_out

        elif self.color == "black" and yaad <= 0:  # the player wants to get piece out of home
            can_out = all(x <= 6 for x in my_pieces)  # checks that all pieces in home
            if str(makor) not in r:
                relevant_roll = [x for x in r if makor <= int(x)]
                if relevant_roll:
                    distance = min(relevant_roll)
                    # all pieces at home and there are no pieces between
                    pieces_between = [x for x in my_pieces if (int(makor) < x <= int(distance))]
                    can_out = can_out and (not pieces_between)
            return can_out

        return no_oponent

    def convert_board_to_pieces_array(self, board):
        pieces = []  # Reset current player pieces
        other_pieces = []  # Reset opposing player pieces

        # Populate self._pieces and self.other_pieces based on board state
        # the first 24
        for i in range(len(board) - 4):
            if board[i] > 0:  # White pieces
                if self.color == "white":
                    pieces.extend([i + 1] * board[i])
                else:
                    other_pieces.extend([i + 1] * board[i])
            elif board[i] < 0:  # Black pieces
                if self.color == "black":
                    pieces.extend([i + 1] * abs(board[i]))
                else:
                    other_pieces.extend([i + 1] * abs(board[i]))

        # the last 4
        if self.color == "black":
            pieces.extend([0] * abs(board[25]))
            pieces.extend([25] * abs(board[27]))
            other_pieces.extend([25] * abs(board[24]))
            other_pieces.extend([0] * abs(board[26]))

        elif self.color == "white":
            other_pieces.extend([0] * board[25])
            other_pieces.extend([25] * board[27])
            pieces.extend([25] * board[24])
            pieces.extend([0] * board[26])

        pieces.sort()  # Ensure pieces are ordered
        other_pieces.sort()

        return pieces, other_pieces

    def create_new_board(self, old_board, move):
        new_board = copy.deepcopy(old_board)
        if self.color == "white":
            if move[0] != 0 and 0 < move[1] < 25:
                new_board[move[0] - 1] -= 1
                new_board[move[1] - 1] += 1
                if old_board[move[1] - 1] == -1:  # white ate black
                    new_board[27] += 1
                    new_board[move[1] - 1] += 1
            if move[0] == 0:  # get eaten white back to game
                new_board[move[1] - 1] += 1
                new_board[26] -= 1
            if move[1] == 25:  # white get out of it's home
                new_board[move[0] - 1] -= 1
                new_board[24] += 1

        elif self.color == "black":
            if move[0] != 25 and 0 < move[1] < 25:
                new_board[move[0] - 1] += 1
                new_board[move[1] - 1] -= 1
                if old_board[move[1] - 1] == 1:  # black ate white
                    new_board[26] += 1
                    new_board[move[1] - 1] -= 1
            if move[0] == 25:  # get eaten black back to game
                new_board[move[1] - 1] -= 1
                new_board[27] -= 1
            if move[1] == 0:  # black get out of it's home
                new_board[move[0] - 1] += 1
                new_board[25] += 1
        return new_board

    def generate_all_moves(self, r, new_board):
        my_pieces, other_pieces = self.convert_board_to_pieces_array(new_board)
        self.all_moves = []

        if self.color == "black" and new_board[27] > 0:  # for black capture pieces
            makor = 25
            yaad = 25 - r
            if self.validMoveRandom(makor, yaad, [r], my_pieces, other_pieces):
                self.all_moves.append([makor, yaad])

        elif self.color == "white" and new_board[26] > 0:  # for white capture pieces
            makor = 0
            yaad = r
            if self.validMoveRandom(makor, yaad, [r], my_pieces, other_pieces):
                self.all_moves.append([makor, yaad])

        else:
            for makor in set(my_pieces):
                if self.color == "black" and makor != 0:
                    yaad = makor - r
                    if yaad < 0:
                        yaad = 0
                    if self.validMoveRandom(makor, yaad, [r], my_pieces, other_pieces):
                        self.all_moves.append([makor, yaad])
                elif self.color == "white" and makor != 25:
                    yaad = makor + r
                    if yaad > 25:
                        yaad = 25
                    if self.validMoveRandom(makor, yaad, [r], my_pieces, other_pieces):
                        self.all_moves.append([makor, yaad])
        return self.all_moves

    def add_move_if_not_exists(self, moves_list, new_move, new_board):
        # Sort individual positions within the new move to ensure uniqueness of the positions
        new_move_check = sorted(new_move)
        # Extract the sub-array of moves (ignoring the board states)
        sub_array = [move[0] for move in moves_list]
        # Check if the sorted new move exists in any orientation (as a tuple)
        for move in sub_array:  # move = [[m1,m2],[m3,m4]]
            move = sorted(move)
            if len(move) == len(new_move_check) and all(move[i] == new_move_check[i] for i in range(len(move))):
                return moves_list

        # new_board = self.create_new_board(new_board, new_move[len(new_move)-1])
        moves_list.append([new_move, new_board])
        return moves_list

    def calculate_all_possible_moves2(self, roll, old_board, moves_list):
        # move_list = [[move1,move2] , new_board]]  ,  move[0] = [move1, move2]   ,  move[1] = new_board
        r1 = roll[0]
        r2 = roll[1]
        all_moves_1 = self.generate_all_moves(r1, old_board)
        for move1 in all_moves_1:
            new_board1 = self.create_new_board(old_board, move1)
            all_moves_2 = self.generate_all_moves(r2, new_board1)
            if not all_moves_2:
                moves_list = self.add_move_if_not_exists(moves_list, [move1], new_board1)
            else:
                for move2 in all_moves_2:
                    new_board2 = self.create_new_board(new_board1, move2)
                    moves_list = self.add_move_if_not_exists(moves_list, [move1, move2], new_board2)
        return moves_list

    def calculate_all_possible_moves4(self, roll, old_board, moves_list):
        r = roll[0]
        all_moves_1 = self.generate_all_moves(r, old_board)
        for move1 in all_moves_1:
            new_board1 = self.create_new_board(old_board, move1)
            all_moves_2 = self.generate_all_moves(r, new_board1)
            if not all_moves_2:
                moves_list = self.add_move_if_not_exists(moves_list, [move1], new_board1)
            else:
                for move2 in all_moves_2:
                    new_board2 = self.create_new_board(new_board1, move2)
                    all_moves_3 = self.generate_all_moves(r, new_board2)
                    if not all_moves_3:
                        moves_list = self.add_move_if_not_exists(moves_list, [move1, move2], new_board2)
                    else:
                        for move3 in all_moves_3:
                            new_board3 = self.create_new_board(new_board2, move3)
                            all_moves_4 = self.generate_all_moves(r, new_board3)
                            if not all_moves_4:
                                moves_list = self.add_move_if_not_exists(moves_list, [move1, move2, move3], new_board3)
                            else:
                                for move4 in all_moves_4:
                                    new_board4 = self.create_new_board(new_board3, move4)
                                    moves_list = self.add_move_if_not_exists(moves_list, [move1, move2, move3, move4],
                                                                             new_board4)
        return moves_list

    def play_random(self, board, roll, color, time_left):
        """Get the board state, dice roll, and player color, and return the chosen move."""
        self.color = color
        self.roll = roll

        # Populate self._pieces and self.other_pieces based on board state
        self._pieces, self.other_pieces = self.convert_board_to_pieces_array(board)

        self.order()  # Ensure pieces are ordered
        self.other_pieces.sort()

        whole_move = self.choose_random_move(roll, board, 1)

        if self.win() or self.lose():
            return whole_move  # Return the best move even if the game is won or lost


        if whole_move is not None:
            for selected_move in whole_move:
                self.move_piece_random(abs(selected_move[1] - selected_move[0]), selected_move[0])

        return whole_move

    def choose_random_move(self, roll, board, print_moves):
        if len(self.roll) == 2:
            moves_list = self.calculate_all_possible_moves2(roll, board, [])
            moves_list = self.calculate_all_possible_moves2(roll[::-1], board, moves_list)
        else:
            moves_list = self.calculate_all_possible_moves4(roll, board, [])
        all_moves = [move[0] for move in moves_list]
        if print_moves:
            print("all possible moves:", sorted(all_moves))

        # Pick a move randomly (can replace with strategic selection)
        if all_moves:
            selected_move = random.choice(all_moves)
        else:
            selected_move = None
        return selected_move


if __name__ == '__main__':
    player = Human_Player()
    p1 = Human_Player()
    p1.set_pieces([])
    assert player.get_pieces() == [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]
    player.move_piece(10, 1, p1)
    assert player.get_pieces() == [1, 11, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]
    print(player)
    try:
        player.move_piece(0, 1, p1)
        print('Error with move_piece')
    except:
        print('move_piece working well with distance')
    try:
        player.move_piece(1, 20, p1)
        print('Error with move_piece')
    except:
        print('move_piece working well with pieces')
    player.set_pieces([0, 0, 0, 1, 0, 0, 0])
    assert player.get_pieces() == [0, 0, 0, 0, 0, 0, 1]
    try:
        player.move_piece(1, 1)
    except:
        print('capturedPiece is working well')
    player.move_piece(1, 0, p1)
    assert player.get_pieces() == [0, 0, 0, 0, 0, 1, 1]
    p1.set_pieces([1, 3, 3, 4, 5])
    player.capture(p1)
    assert p1.get_pieces() == [3, 3, 4, 5, 25]
    p1.set_pieces([2, 2])
    assert player.validMove(2, p1) == False
    assert player.validMove(3, p1) == True
    p1.set_pieces([5, 5])
    try:
        player.move_piece(4, 1, p1)
    except:
        print('validMove is working inside of move_piece')
    player.move_piece(4, 0, p1)
    assert player.get_pieces() == [0, 0, 0, 0, 1, 1, 4]
    player.set_pieces([25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25])
    assert player.win() == True

    print('All tests passed')
