import chess.pgn
import multiprocessing as mp
import numpy as np

class DataExtractor:
    def __init__(self, file):
        self.file = file

    def process_game(self, game):
        fen, moves = [], []
        board = game.board()
        for move in game.mainline_moves():
            fen.append(board.fen())
            moves.append(move.uci())
            board.push(move)

        return fen, moves
    
    def extract_pgn(self, no_of_games=None, batch_size=100000):
        games_processed = 0
        fen_chunk = []
        move_chunk = []
        pgn = open(self.file)

        with mp.Pool(mp.cpu_count()) as pool:
            while True:
                games = [chess.pgn.read_game(pgn) for _ in range(mp.cpu_count())]
                
                if not games:
                    break

                results = pool.map(self.process_game, games)

                for fens, moves in results:
                    fen_chunk.extend(fens)
                    move_chunk.extend(moves)

                games_processed += len(games)

                if len(fen_chunk) >= batch_size:
                    np.savez_compressed(f"fen_{games_processed}.npz", fens=fen_chunk, moves=move_chunk)

                    fen_chunk.clear()
                    move_chunk.clear()

                print(f"Processed {games_processed} games...")

                if no_of_games is not None and games_processed >= no_of_games:
                    break

        if fen_chunk:
            np.savez_compressed(f"fen_{games_processed}.npz", fens=fen_chunk, moves=move_chunk)

        print("Completed extraction")

if __name__ == "__main__":
    file = ""
    load_data = DataExtractor(file)

    load_data.extract_pgn()