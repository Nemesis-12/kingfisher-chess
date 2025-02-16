import chess
import chess.pgn

def export_pgn(game):
    with open("game.pgn", "w") as file:
        export = chess.pgn.FileExporter(file)
        game.accept(export)