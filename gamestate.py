from message import Message

class GameState:
    WIDTH = 7
    HEIGHT = 6
    A = "A"
    B = "B"
    EMPTY = "-"

    def __init__(self):
        self.player_a = None
        self.player_b = None
        self.opponent = ""
        self.symbol = None
        self.turn = GameState.A
        self.board = [[GameState.EMPTY for y in range(GameState.HEIGHT)] for x in range(GameState.WIDTH)]

    # Apply a message, on a server
    def apply_message_server(self, message, manager):
        match message.message_type:
            case Message.MOVE:
                # Log the move request
                print("Move sent by player (" + manager.player.name + "): " + message.content)
                # Check if the game has even begun
                if(self.player_a is None or self.player_b is None):
                    print("Game has not yet begun. Rejecting.")
                    manager.schedule_message(Message(Message.HALT, "Game has not yet begun. Please wait for the game to begin.").pack())
                    return
                # Check if it is even their turn
                if(not self.is_player_turn(manager)):
                    print("Not the current player turn. Rejecting.")
                    manager.schedule_message(Message(Message.HALT, "Move requested out of turn. Please wait for your turn.").pack())
                    return
                
                # Parse the request
                try:
                    column = int(message.content)
                    if(column < 1 or column > 7):
                        raise ValueError('Column out of range.')
                except(ValueError):
                    # Catch non-number request
                    print("Invalid move. Rejecting.")
                    manager.schedule_message(Message(Message.REDO, self.turn + ":Invalid move request. Please try again.").pack())
                    return
                
                row = self.get_move_from_column(column)
                x = column - 1
                y = row - 1

                # Check if the move is legal
                if(x < 0 or x > GameState.WIDTH-1 or y < 0 or y > GameState.HEIGHT - 1 or self.board[x][y] != GameState.EMPTY):
                    print("Illegal move. Rejecting.")
                    manager.schedule_message(Message(Message.REDO, self.turn + ":Illegal move request. Please try again.").pack())
                    return
                # Perform the move, inform the clients
                self.board[x][y] = GameState.A if self.player_a == manager else GameState.B
                self.broadcast_board(self.player_a)
                self.broadcast_board(self.player_b)

                # Check for win conditions
                if(self.check_win()):
                    self.broadcast_to_players(Message(Message.OVER, manager.player.name + " has won!").pack())
                    self.wipe_game()
                elif(self.check_draw()):
                    self.broadcast_to_players(Message(Message.OVER, "It's a draw!").pack())
                    self.wipe_game()
                else:
                    # Swap the turn
                    self.swap_turn()

    # Send the board state through the given manager
    def broadcast_board(self, manager):
        manager.schedule_message(Message(Message.STAT, self.pack_board()).pack())


    # Determine the move row for a given column
    def get_move_from_column(self, column):
        for y in range(0, GameState.HEIGHT):
            if(self.board[column-1][y] != GameState.EMPTY):
                return y # y-1 is the INDEX, but we're returning the ROW, which is 1 indexed
        return GameState.HEIGHT


    # Get the player symbol for the given manager
    def get_player_symbol(self, manager):
        if(self.player_a == manager):
            return GameState.A
        if(self.player_b == manager):
            return GameState.B
        return None
    

    # Send the name of the opponent using a NAME message
    def send_opponent_name(self):
        self.player_a.schedule_message(Message(Message.NAME, self.player_b.player.name).pack())
        self.player_b.schedule_message(Message(Message.NAME, self.player_a.player.name).pack())

    
    # Send the full opponent player data
    def send_opponent_player(self, manager):
        if(self.player_a == manager):
            self.player_a.schedule_message(Message(Message.PLYR, self.player_b.player.pack()).pack())
        if(self.player_a == manager):
            self.player_b.schedule_message(Message(Message.PLYR, self.player_a.player.pack()).pack())


    # Determine if it is currently the turn of the given manager
    def is_player_turn(self, manager):
        if((self.turn == GameState.A and self.player_b == manager) or (self.turn == GameState.B and self.player_a == manager)):
            return False
        return True


    # Swap the current turn state, and inform the players
    def swap_turn(self):
        if(self.turn == GameState.A):
            self.turn = GameState.B
            self.broadcast_to_players(Message(Message.TURN, GameState.B).pack())
        else:
            self.turn = GameState.A
            self.broadcast_to_players(Message(Message.TURN, GameState.A).pack())

    
    # Pack the board data into a string
    def pack_board(self):
        packed = ""
        for x in range(0, GameState.WIDTH):
            for y in range(0, GameState.HEIGHT):
                packed += self.board[x][y]
        return packed
    

    # Unpack the board data from a string
    def unpack_board(self, packed):
        index = 0
        for x in range(0, GameState.WIDTH):
            for y in range(0, GameState.HEIGHT):
                self.board[x][y] = packed[index]
                index += 1


    # Print the current board data
    def print_board(self):
        print("A - " + self.player_a.name)
        print("B - " + self.player_b.name)
        print(" 1 2 3 4 5 6 7")
        print(" -------------")
        for y in range(0, GameState.HEIGHT):
            print("|", end='')
            for x in range(0, GameState.WIDTH):
                print(self.board[x][y], end='')
                if(x < GameState.WIDTH-1):
                    print(" ", end='')
            print("|")
        print(" -------------")


    # Broadcast a message to both players
    def broadcast_to_players(self, message):
        self.player_a.schedule_message(message)
        self.player_b.schedule_message(message)

    
    # Check for the win condition
    def check_win(self):
        for y in range(0, GameState.HEIGHT):
            for x in range(0, GameState.WIDTH):
                base_value = self.board[x][y]
                if(base_value == GameState.EMPTY):
                    continue
                for dir in range(0, 8):
                    dx, dy = self.get_direction(dir)
                    for step in range(1, 4):
                        check_x = x + (dx * step)
                        check_y = y + (dy * step)
                        if(check_x < 0 or check_x >= GameState.WIDTH or check_y < 0 or check_y >= GameState.HEIGHT):
                            break
                        check_value = self.board[check_x][check_y]
                        if(base_value != check_value):
                            break
                        if(step == 3):
                            return True
        return False
    

    # Check for draw conditions. This assumes win conditions have already been checked for.
    def check_draw(self):
        for y in range(0, GameState.HEIGHT):
            for x in range(0, GameState.WIDTH):
                if(self.board[x][y] == GameState.EMPTY):
                    return False
        return True
    

    def wipe_game(self):
        self.player_a.game_state = None
        self.player_b.game_state = None


    def get_direction(self, dir):
        dx = 0
        dy = 0
        match dir:
            case 0:
                dx = 0
                dy = -1
            case 1:
                dx = 1
                dy = -1
            case 2:
                dx = 1
                dy = 0
            case 3:
                dx = 1
                dy = 1
            case 4:
                dx = 0
                dy = 1
            case 5:
                dx = -1
                dy = 1
            case 6:
                dx = -1
                dy = 0
            case 7:
                dx = -1
                dy = -1
        return (dx, dy)


    # Apply a message, on a client
    def apply_message_client(self, message):
        match message.message_type:
            case Message.WAIT:
                print("Waiting for a match...")
            case Message.NAME:
                print("Opponent found: " + message.content)
            case Message.PLAY:
                print("Play begins!")
            case Message.TURN:
                print("Turn change!")
                self.turn = GameState.A if message.content == GameState.A else GameState.B
            case Message.STAT:
                print("Board updated!")
                self.unpack_board(message.content)
                self.print_board()
            case Message.MOVE:
                pass