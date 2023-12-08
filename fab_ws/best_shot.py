import math
from pprint import pprint

import numpy as np

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

class PoolSimulator:
    def __init__(self, cue_ball, holes, player1_balls, player2_balls, radius):
        """
        :param holes: set of (x, y) coordinates of the holes
        :param player1_balls: set of (x, y) coordinates of player 1's balls
        :param player2_balls: set of (x, y) coordinates of player 2's balls
        :param radius: radius of the balls
        """
        self.holes = holes
        self.radius = radius
        self.cue_ball = cue_ball

        self.player1_balls = player1_balls
        self.player2_balls = player2_balls
        self.all_balls = {cue_ball} | player1_balls | player2_balls

    def is_path_clear(self, b1, b2):
        """
        Check if the path between two balls is clear.

        NOTE: If this is a bottleneck, we could implment this circle-line 
        intersection algorithm: https://mathworld.wolfram.com/Circle-LineIntersection.html
        """
        num_samples = 500
        x1, y1 = b1
        x2, y2 = b2

        # Check if the path between the balls is clear
        for ball in self.all_balls:
            # skip the balls we're checking against and the cue ball
            if ball == b1 or ball == b2:
                continue

            # sample points along the line between the balls
            # and check if any of them are within the radius of the ball
            for t in np.linspace(0, 1, num_samples):
                x_sample = x1 + t*(x2 - x1)
                y_sample = y1 + t*(y2 - y1)
                if distance((x_sample, y_sample), ball) <= 2*self.radius:
                    return False

        return True

    def _get_target_pos(self, player_ball, hole):
        """
        Find the target position for the player ball to make the shot.
        """
        x1, y1 = player_ball
        x2, y2 = hole
        dist = distance(player_ball, hole)

        # position the target ball 2*radius away from the hole
        dx = (2*self.radius / dist) * (x1 - x2)
        dy = (2*self.radius / dist) * (y1 - y2)
        x = x1 + dx
        y = y1 + dy

        return x, y

    def get_best_shot(self, player1=True):
        """
        Returns the best target coordinate for the cue ball to aim for.
        """
        player_balls = self.player1_balls if player1 else self.player2_balls

        # Find all possible shots from target balls to holes
        possible_shots = []
        for player_ball in player_balls:
            for hole in self.holes:
                if self.is_path_clear(player_ball, hole):
                    possible_shots.append((player_ball, hole))

        # Evaluate each shot based on distance from the hole            
        possible_shots.sort(key=lambda shot: distance(shot[0], shot[1]))
        # print('all possible shots:'); pprint(possible_shots)

        # Find the best shot that the cue ball can hit
        for shot in possible_shots:
            # Find the target position to make the shot
            player_ball, hole = shot
            target_coor = self._get_target_pos(player_ball, hole)

            # Return first shot that the cue ball can hit
            if self.is_path_clear(self.cue_ball, target_coor):
                # print('best shot:', shot)
                return target_coor

        print('No possible shot found')
        return None

# Setup:
holes = {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)}
radius = 0.05

# Test case 1: obvious shot
cue_ball = (1, 0.5)
player1_balls = {(1, 0.75)}
player2_balls = set()
pool = PoolSimulator(cue_ball, holes, player1_balls, player2_balls, radius)

best_shot = pool.get_best_shot(player1=True)

# Test case 2: ignore player 2 balls
cue_ball = (1, 0.5)
player1_balls = {(1, 0.65)}
player2_balls = {(1, 0.9)}
pool = PoolSimulator(cue_ball, holes, player1_balls, player2_balls, radius)

best_shot = pool.get_best_shot(player1=True)

# Test case 3: opponent ball in optimal way
cue_ball = (1, 0.5)
player1_balls = {(1, 0.9)}
player2_balls = {(1, 0.65)}
pool = PoolSimulator(cue_ball, holes, player1_balls, player2_balls, radius)

best_shot = pool.get_best_shot(player1=True)

# Test case 4: general case
cue_ball = (1, 0.5)
player1_balls = {
    (1, 0.9), 
    (1.2, 0.7), 
    (1.6, 0.7), 
    (1.85, 0.5),
    (0.2, 0.2),
}
player2_balls = {
    (1, 0.65),
    (1.4, 0.65)
}
pool = PoolSimulator(cue_ball, holes, player1_balls, player2_balls, radius)

best_shot = pool.get_best_shot(player1=True)
print(best_shot)