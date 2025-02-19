import chess.pgn
import pandas as pd
from encoder import Encoder
import multiprocessing as mp

class DataExtractor:
    def __init__(self, file):
        self.file = file
        self.encoder = Encoder()

    def process_game(self, game):
        features = []
        labels = []
        board = game.board()
        for move in game.mainline_moves():
            features.append(self.encoder.encode(board).flatten())
            labels.append(move.uci())
            board.push(move)

        return features, labels
    
    def extract_pgn(self, no_of_games=None, batch_size=100000):
        games_processed = 0
        chunk_features = []
        chunk_labels = []
        pgn = open(self.file)

        with mp.Pool(mp.cpu_count()) as pool:
            while True:
                games = [chess.pgn.read_game(pgn) for _ in range(mp.cpu_count())]
                
                if not games:
                    break

                results = pool.map(self.process_game, games)

                for features, labels in results:
                    chunk_features.extend(features)
                    chunk_labels.extend(labels)

                games_processed += len(games)

                if len(chunk_features) >= batch_size:
                    feature_df = pd.DataFrame(chunk_features)
                    label_df = pd.DataFrame(chunk_labels, columns=["Moves"])

                    feature_df.to_csv("features.csv", mode="a", index=False)
                    label_df.to_csv("labels.csv", mode="a", index=False)

                    chunk_features.clear()
                    chunk_labels.clear()

                print(f"Processed {games_processed} games...")

                if no_of_games is not None and games_processed >= no_of_games:
                    break

        if chunk_features:
            feature_df = pd.DataFrame(chunk_features)
            label_df = pd.DataFrame(chunk_labels, columns=["Moves"])

            feature_df.to_csv("features.csv", mode="a", index=False)
            label_df.to_csv("labels.csv", mode="a", index=False)

        print("Completed extraction")

if __name__ == "__main__":
    file = ""
    load_data = DataExtractor(file)

    load_data.extract_pgn()