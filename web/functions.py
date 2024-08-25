def get_random_gradient():
    import random
    r1, g1, b1 = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    r2, g2, b2 = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    return f'radial-gradient(circle, rgba({r1},{g1},{b1},1) 0%, rgba({r2},{g2},{b2},1) 100%)'