import pygame as pg
import sys

def text_generator(text):
    tmp = ''
    for letter in text:
        tmp += letter
        yield tmp

class dynamic_text:
    def __init__(self, font, text, pos, autoreset=False):
        self.done = False
        self.font = font
        self.text = text.split('\n')
        self.pos = pos
        self.autoreset = autoreset
        self.current_line = 0
        self._gen = text_generator(self.text[self.current_line])
        self.rendered_lines = []
        self.update()

    def reset(self):
        self._gen = text_generator(self.text[self.current_line])
        self.done = False
        self.rendered_lines = []
        self.update()

    def update(self):
        if not self.done:
            try:
                self.rendered_lines.append(self.font.render(next(self._gen), True, (0, 128, 0)))
            except StopIteration:
                self.current_line += 1
                if self.current_line < len(self.text):
                    self._gen = text_generator(self.text[self.current_line])
                else:
                    self.done = True
                    if self.autoreset:
                        self.current_line = 0
                        self.reset()

    def draw(self, screen):
        y_offset = 0
        for line in self.rendered_lines:
            screen.blit(line, (self.pos[0], self.pos[1] + y_offset))
            y_offset += self.font.get_height()
    def update(self):
        if not self.done:
            try:
                self.rendered_lines.append(self.font.render(next(self._gen), True, (0, 128, 0)))
            except StopIteration:
                self.current_line += 1
                if self.current_line < len(self.text):
                    self._gen = text_generator(self.text[self.current_line])
                else:
                    self.done = True
                    if self.autoreset:
                        self.current_line = 0
                        self.reset()

    def draw(self, screen):
        y_offset = 0
        for line in self.rendered_lines:
            screen.blit(line, (self.pos[0], self.pos[1] + y_offset))
            y_offset += self.font.get_height()

class Intro:
    def __init__(self, screen):
        self.SCREEN = screen
        self.background = pg.image.load("resources/backgrounds/acadhall.jpg").convert()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 25)
        self.text = (
            "Your journey begins in the halls of Mapúa University, where an exciting challenge is about to unfold. "
            "The school has just announced the Typing Championship, a high-stakes competition where only the fastest "
            "and most precise typists will have the chance to represent their institution.\n\n"
            "At first, you didn’t think much of it. After all, it’s just typing, right? You’ve spent hours playing online "
            "typing games, casually testing your speed, maybe even winning a few friendly arguments—but this is different. "
            "This is a real competition, against real opponents, with real stakes.\n\n"
            "Word spreads fast. Whispers in the classroom, hushed conversations in the hallway—who will step up? Your name "
            "comes up, but you’re not the only one being watched. The school’s top writer, known for dominating competitions, "
            "has their eyes set on the prize. And then there’s the rival, determined to outmatch everyone, no matter what it takes.\n\n"
            "With each round, the challenges grow tougher. You’ll go from competing against classmates to facing the best typists "
            "from all across the university—people who have been training for this moment for years. Some will underestimate you. "
            "Others will do whatever it takes to win. But one thing is certain: every keystroke counts.\n\n"
            "This is your chance to prove yourself. To rise above the competition. To become Mapúa University’s Fastest Typist.\n\n"
            "Do you have what it takes? Let the Typing Championship begin!"
        )
        self.message = dynamic_text(self.font, self.text, (50, 50), autoreset=False)
        self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
        self.skip_rect = self.skip_prompt.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.USEREVENT:
                    self.message.update()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    return True

            self.SCREEN.blit(self.background, (0, 0))
            self.message.draw(self.SCREEN)
            self.SCREEN.blit(self.skip_prompt, self.skip_rect)
            pg.display.flip()
            pg.time.Clock().tick(60)