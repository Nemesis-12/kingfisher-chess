import chess.pgn
import numpy as np
import pandas as pd
from encoder import Encoder

class DataExtractor:
    def __init__(self, file):
        self.file = file
    
    def extract_pgn(self, no_of_games=None):
        features = []
        labels = []
        encoded_board = Encoder()

        with open(self.file) as pgn:
            games_processed = 0

            while True:
                game = chess.pgn.read_game(pgn)
                
                if game is None:
                    break

                board = game.board()
                for move in game.mainline_moves():
                    features.append(encoded_board.encode(board))
                    labels.append(move.uci())
                    board.push(move)

                games_processed += 1
                if no_of_games is not None and games_processed >= no_of_games:
                    break           

        feature_data = np.array(features).reshape(len(features), -1)
        label_data = np.array(labels).reshape(-1, 1)

        feature_df = pd.DataFrame(feature_data)
        label_df = pd.DataFrame(label_data, columns=["Moves"])

        feature_df.to_csv("features.csv", index=False)
        label_df.to_csv("labels.csv", index=False)

        print("Created features.csv and labels.csv")