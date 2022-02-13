import logging

logger = logging.getLogger(__name__)


class Conversation:
    def __init__(self, game, engine, xhr, version, challenge_queue):
        self.game = game
        self.engine = engine
        self.xhr = xhr
        self.version = version
        self.challengers = challenge_queue

    command_prefix = "!"

    def react(self, line, game):
        logger.info("*** {} [{}] {}: {}".format(self.game.url(), line.room, line.username, line.text.encode("utf-8")))
        if (line.text[0] == self.command_prefix):
            self.command(line, game, line.text[1:].lower())

    def command(self, line, game, cmd):
        if cmd == "commands" or cmd == "help":
            self.send_reply(line, "Supported commands: !wait (wait a minute for my first move), !name, !howto, !eval, !queue")
        elif cmd == "wait" and game.is_abortable():
            game.ping(60, 120, 120)
            self.send_reply(line, "Waiting 60 seconds...")
             elif cmd == "name":
            name = game.me.name
            self.send_reply(line, "{} running {} (lichess-bot v{})".format(name, self.engine.name(), self.version))
        elif cmd == "howto":
            self.send_reply(line, "How to run: Check out 'Lichess Bot API'")
        elif cmd == "eval" and line.room == "spectator":
            stats = self.engine.get_stats(for_chat=True)
            self.send_reply(line, ", ".join(stats))
        elif cmd == "eval":
            self.send_reply(line, "I don't tell that to my opponent, sorry.")
        elif cmd == "queue":
            if self.challengers:
                challengers = ", ".join(["@" + challenger.challenger_name for challenger in reversed(self.challengers)])
                self.send_reply(line, "Challenge queue: {}".format(challengers))
            else:
                self.send_reply(line, "No challenges queued.")
        elif command == 'draw':
            return self.draw_message

        if not draw_enabled:
            return 'This bot will neither accept nor offer draws.'

        min_game_length = config['engine']['offer_draw']['min_game_length']
        max_score = config['engine']['offer_draw']['score'] / 100
        consecutive_moves = config['engine']['offer_draw']['consecutive_moves']

        return f'The bot offers draw at move {min_game_length} or later ' \
            f'if the eval is within +{max_score:.2f} to -{max_score:.2f} for the last {consecutive_moves} moves.'
    
  

    def send_reply(self, line, reply):
        self.xhr.chat(self.game.id, line.room, reply)

    def send_message(self, room, message):
        if message:
            self.send_reply(ChatLine({"room": room}), message)


class ChatLine:
    def __init__(self, json):
        self.room = json.get("room")
        self.username = json.get("username")
        self.text = json.get("text")
