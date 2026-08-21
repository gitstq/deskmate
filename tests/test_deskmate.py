"""
单元测试 / Unit tests
测试宠物状态机、番茄钟、配置管理等核心逻辑（无需GUI环境）
Test pet state machine, pomodoro, config manager etc. (no GUI environment needed)
"""

import unittest
import os
import sys
import tempfile
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPetStats(unittest.TestCase):
    """测试宠物属性 / Test pet stats"""

    def test_clamp(self):
        from deskmate.pet import PetStats
        stats = PetStats(hunger=150, happiness=-10, energy=200, cleanliness=-50)
        stats.clamp()
        self.assertEqual(stats.hunger, 100)
        self.assertEqual(stats.happiness, 0)
        self.assertEqual(stats.energy, 100)
        self.assertEqual(stats.cleanliness, 0)

    def test_overall_mood(self):
        from deskmate.pet import PetStats, Mood
        stats = PetStats(hunger=90, happiness=90, energy=90, cleanliness=90)
        self.assertEqual(stats.overall_mood, Mood.VERY_HAPPY)
        stats = PetStats(hunger=20, happiness=20, energy=20, cleanliness=20)
        self.assertEqual(stats.overall_mood, Mood.SAD)


class TestBasePet(unittest.TestCase):
    """测试宠物基类行为 / Test base pet behavior"""

    def setUp(self):
        from deskmate.pet import BasePet, PetState
        self.BasePet = BasePet
        self.PetState = PetState
        # 使用一个简单的子类进行测试 / Use a simple subclass for testing
        class TestPet(BasePet):
            def draw(self, painter, x, y, scale=1.0):
                pass
        self.TestPet = TestPet

    def test_initial_state(self):
        pet = self.TestPet("Test")
        self.assertEqual(pet.state, self.PetState.IDLE)
        self.assertEqual(pet.name, "Test")

    def test_feed(self):
        pet = self.TestPet("Test")
        pet.stats.hunger = 30
        pet.feed()
        self.assertEqual(pet.state, self.PetState.EATING)
        self.assertGreater(pet.stats.hunger, 30)

    def test_play(self):
        pet = self.TestPet("Test")
        initial_happiness = pet.stats.happiness
        initial_energy = pet.stats.energy
        pet.play()
        self.assertEqual(pet.state, self.PetState.PLAYING)
        self.assertGreater(pet.stats.happiness, initial_happiness)
        self.assertLess(pet.stats.energy, initial_energy)

    def test_sleep(self):
        pet = self.TestPet("Test")
        pet.stats.energy = 30
        pet.sleep()
        self.assertEqual(pet.state, self.PetState.SLEEPING)
        self.assertGreater(pet.stats.energy, 30)

    def test_pet(self):
        pet = self.TestPet("Test")
        initial = pet.stats.happiness
        pet.pet()
        self.assertEqual(pet.state, self.PetState.HAPPY)
        self.assertGreater(pet.stats.happiness, initial)

    def test_clean(self):
        pet = self.TestPet("Test")
        pet.stats.cleanliness = 20
        pet.clean()
        self.assertEqual(pet.stats.cleanliness, 100)

    def test_speak(self):
        pet = self.TestPet("Test")
        pet.speak("Hello")
        self.assertEqual(pet.speech_text, "Hello")
        self.assertGreater(pet.speech_until, time.time())

    def test_change_state(self):
        pet = self.TestPet("Test")
        callback_called = []
        pet.on_state_change = lambda old, new: callback_called.append((old, new))
        pet.change_state(self.PetState.WALKING, 3)
        self.assertEqual(pet.state, self.PetState.WALKING)
        self.assertEqual(len(callback_called), 1)

    def test_walking_movement(self):
        pet = self.TestPet("Test")
        pet.x = 100
        pet.target_x = 200
        pet.speed = 10
        pet.change_state(self.PetState.WALKING, 10)
        pet.update(0.1, 800, 600)
        self.assertGreater(pet.x, 100)


class TestPomodoro(unittest.TestCase):
    """测试番茄钟 / Test pomodoro timer"""

    def setUp(self):
        from deskmate.utils.pomodoro import PomodoroTimer, PomodoroState
        self.PomodoroTimer = PomodoroTimer
        self.PomodoroState = PomodoroState

    def test_initial_state(self):
        timer = self.PomodoroTimer(25, 5)
        self.assertEqual(timer.state, self.PomodoroState.IDLE)
        self.assertEqual(timer.remaining, 25 * 60)

    def test_start(self):
        timer = self.PomodoroTimer(25, 5)
        timer.start()
        self.assertEqual(timer.state, self.PomodoroState.WORKING)

    def test_pause_resume(self):
        timer = self.PomodoroTimer(25, 5)
        timer.start()
        timer.pause()
        self.assertEqual(timer.state, self.PomodoroState.PAUSED)
        timer.resume()
        self.assertEqual(timer.state, self.PomodoroState.WORKING)

    def test_stop(self):
        timer = self.PomodoroTimer(25, 5)
        timer.start()
        timer.stop()
        self.assertEqual(timer.state, self.PomodoroState.IDLE)
        self.assertEqual(timer.completed_cycles, 0)

    def test_format_time(self):
        timer = self.PomodoroTimer(25, 5)
        timer.remaining = 1500  # 25:00
        self.assertEqual(timer.format_time(), "25:00")
        timer.remaining = 65
        self.assertEqual(timer.format_time(), "01:05")

    def test_progress(self):
        timer = self.PomodoroTimer(10, 5)
        timer.remaining = 300  # half of 600 seconds
        timer.state = self.PomodoroState.WORKING
        self.assertAlmostEqual(timer.progress, 0.5, places=1)

    def test_work_complete_callback(self):
        timer = self.PomodoroTimer(1, 1)  # 1 minute work, 1 minute break
        completed = []
        timer.on_work_complete = lambda: completed.append(True)
        timer.start()
        timer.remaining = 0.01
        timer._last_tick = time.time() - 1
        timer.update()
        self.assertEqual(timer.state, self.PomodoroState.ON_BREAK)
        self.assertEqual(timer.completed_cycles, 1)


class TestConfigManager(unittest.TestCase):
    """测试配置管理 / Test config manager"""

    def setUp(self):
        from deskmate.utils.config import ConfigManager
        self.ConfigManager = ConfigManager
        self.tmpdir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.tmpdir, "test_config.json")

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.tmpdir)

    def test_default_config(self):
        mgr = self.ConfigManager(self.config_path)
        self.assertEqual(mgr.config.pet_species, "cat")
        self.assertEqual(mgr.config.scale, 1.0)
        self.assertTrue(mgr.config.enable_pomodoro)

    def test_save_and_load(self):
        mgr = self.ConfigManager(self.config_path)
        mgr.update(pet_species="dog", pet_name="Rex", scale=1.5)
        # 重新加载 / Reload
        mgr2 = self.ConfigManager(self.config_path)
        self.assertEqual(mgr2.config.pet_species, "dog")
        self.assertEqual(mgr2.config.pet_name, "Rex")
        self.assertEqual(mgr2.config.scale, 1.5)

    def test_corrupted_config(self):
        # 写入损坏的JSON / Write corrupted JSON
        with open(self.config_path, "w") as f:
            f.write("{invalid json")
        mgr = self.ConfigManager(self.config_path)
        # 应该回退到默认值 / Should fall back to defaults
        self.assertEqual(mgr.config.pet_species, "cat")

    def test_get(self):
        mgr = self.ConfigManager(self.config_path)
        self.assertEqual(mgr.get("pet_species"), "cat")
        self.assertIsNone(mgr.get("nonexistent"))
        self.assertEqual(mgr.get("nonexistent", "default"), "default")


class TestPetRegistry(unittest.TestCase):
    """测试宠物注册表 / Test pet registry"""

    def test_all_pets_creatable(self):
        from deskmate.pets import create_pet, PET_REGISTRY
        for species in PET_REGISTRY:
            pet = create_pet(species, "Test")
            self.assertIsNotNone(pet)
            self.assertEqual(pet.SPECIES_NAME, species)

    def test_unknown_species_raises(self):
        from deskmate.pets import create_pet
        with self.assertRaises(ValueError):
            create_pet("dragon", "Test")


class TestSystemMonitor(unittest.TestCase):
    """测试系统监控 / Test system monitor"""

    def test_get_cpu_returns_float(self):
        from deskmate.utils.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        # 第一次调用可能返回0（需要两次采样）/ First call may return 0 (needs two samples)
        usage = monitor.get_cpu_usage()
        self.assertIsInstance(usage, float)
        self.assertGreaterEqual(usage, 0.0)
        self.assertLessEqual(usage, 100.0)

    def test_get_memory_returns_float(self):
        from deskmate.utils.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        usage = monitor.get_memory_usage()
        self.assertIsInstance(usage, float)
        self.assertGreaterEqual(usage, 0.0)
        self.assertLessEqual(usage, 100.0)

    def test_status_text(self):
        from deskmate.utils.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        text = monitor.get_status_text()
        self.assertIn("CPU", text)
        self.assertIn("MEM", text)


if __name__ == "__main__":
    unittest.main()
