from cs2esp.lib.vec3 import Vec3


def test_distance():
    a = Vec3(0, 0, 0)
    b = Vec3(3, 4, 0)
    assert a.distance_to(b) == 5.0


def test_sub():
    a = Vec3(5, 5, 5)
    b = Vec3(1, 1, 1)
    d = a - b
    assert (d.x, d.y, d.z) == (4, 4, 4)


def test_to_screen_behind_camera():
    m = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0]
    assert Vec3(0, 0, 1).to_screen(m, 1920, 1080) is None