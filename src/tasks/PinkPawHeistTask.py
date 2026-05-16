import time

import cv2
import numpy as np
from ok import TaskDisabledException
from qfluentwidgets import FluentIcon

from src.tasks.BaseNTETask import BaseNTETask
from src.tasks.NTEOneTimeTask import NTEOneTimeTask


class PinkPawHeistTask(NTEOneTimeTask, BaseNTETask):
    CONF_LOOP_COUNT = "循环次数"
    CONF_SCHEME = "地图方案"

    SCHEME_CORE1 = "方案一(Core1)"

    BASE_WIDTH = 1280
    BASE_HEIGHT = 720

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "粉爪大劫案自动化"
        self.description = "移植 MaaNTE 方案一（Core1）的粉爪自动跑图/战斗/撤离流程"
        self.icon = FluentIcon.GAME
        self.support_schedule_task = True
        self.default_config.update(
            {
                self.CONF_LOOP_COUNT: 1,
                self.CONF_SCHEME: self.SCHEME_CORE1,
            }
        )
        self.config_type.update(
            {
                self.CONF_SCHEME: {
                    "type": "drop_down",
                    "options": [self.SCHEME_CORE1],
                },
            }
        )
        self.config_description.update(
            {
                self.CONF_LOOP_COUNT: "执行粉爪流程的次数",
                self.CONF_SCHEME: "当前仅支持移植的 Core1 方案",
            }
        )
        self.add_exit_after_config()

    def run(self):
        super().run()
        try:
            self.do_run()
        except TaskDisabledException:
            pass

    def do_run(self):
        loop_count = self._get_loop_count()
        scheme = self.config.get(self.CONF_SCHEME, self.SCHEME_CORE1)

        self.log_info(f"开始执行粉爪大劫案自动化，方案={scheme}，循环={loop_count}")
        for i in range(loop_count):
            self.info_set("当前轮次", f"{i + 1}/{loop_count}")
            self.log_info(f"开始第 {i + 1}/{loop_count} 轮")

            if not self._enter_heist():
                self.log_error("进入粉爪副本失败", notify=True)
                raise TaskDisabledException("进入粉爪副本失败")

            if scheme == self.SCHEME_CORE1:
                if not self._run_core1_scheme():
                    self._exit_to_main()
                    raise TaskDisabledException("粉爪 Core1 执行失败")

            if not self._evacuate_once():
                self._exit_to_main()
                raise TaskDisabledException("粉爪撤离失败")

            self.log_info(f"第 {i + 1}/{loop_count} 轮执行结束")

        self.log_info("粉爪大劫案自动化执行完成", notify=True)

    def _get_loop_count(self) -> int:
        try:
            loop_count = int(self.config.get(self.CONF_LOOP_COUNT, 1))
        except (TypeError, ValueError):
            loop_count = 1
        return max(1, loop_count)

    def _run_core1_scheme(self) -> bool:
        self._switch_role("3", repeat=3)

        self._key_down("w")
        self.sleep(4.5)
        self._key_down("d")
        self.sleep(3.4)
        self._key_up("d")
        self.sleep(2)
        self._key_up("w")
        self._tap_key("f")
        self.sleep(4)

        self._key_down("w")
        self.sleep(1.5)
        self._key_down("d")
        self.sleep(0.3)
        self._key_up("d")
        self._tap_repeat("space", 20, 0.2)
        self._key_up("w")
        self.sleep(0.1)
        self._key_down("s")
        self.sleep(0.7)
        self._key_up("s")

        self.log_info("等待 G 层战斗1")
        self._switch_role("1", repeat=3)
        if not self._fight_until_no_monster(
            timeout_no_monster=10,
            wait_for_monster=True,
            role_to_switch_back="3",
            loot=False,
            attack_cycles=3,
        ):
            return False

        self._key_down("w")
        self.sleep(4)
        self._key_up("w")
        self.sleep(0.5)
        self._key_down("s")
        self.sleep(0.6)
        self._key_up("s")
        self.sleep(0.2)
        self._key_down("d")
        self.sleep(3.4)
        self._key_up("d")
        self.sleep(0.2)
        self._key_down("a")
        self.sleep(0.2)
        self._key_up("a")
        self.sleep(0.2)

        self._key_down("s")
        self._tap_repeat("f", 22, 0.3)
        self._key_up("s")
        self.sleep(0.5)

        self._key_down("a")
        self.sleep(0.7)
        self._key_up("a")
        self.sleep(0.2)

        self._key_down("w")
        self._tap_repeat("f", 13, 0.3)
        self._key_up("w")
        self.sleep(0.5)

        self._key_down("w")
        self.sleep(2.5)
        self._key_up("w")
        self.sleep(0.2)
        self._tap_key("space")
        self.sleep(0.5)

        self._key_down("s")
        self.sleep(1)
        self._key_up("s")
        self._key_down("a")
        self.sleep(0.5)
        self._tap_repeat("f", 40, 0.1)
        self._key_up("a")

        self._key_down("s")
        self.sleep(0.5)
        self._key_down("d")
        self.sleep(0.06)
        self._key_up("d")
        self._tap_repeat("f", 12, 0.3)
        self._key_up("s")
        self.sleep(0.5)
        self._key_down("d")
        self.sleep(0.75)
        self._key_up("d")

        self._key_down("w")
        self._tap_repeat("f", 22, 0.3)
        self._key_up("w")
        self.sleep(0.5)

        self._key_down("d")
        self._tap_repeat("f", 16, 0.3)
        self._key_up("d")
        self.sleep(0.5)

        self._tap_key("f")
        self.sleep(0.3)
        self._tap_key("f")
        self.sleep(1)

        self.sleep(3)
        self._key_down("w")
        self.sleep(2.3)
        self._key_down("a")
        self.sleep(2)
        self._key_up("a")
        self.sleep(1.5)
        self._key_up("w")
        self.sleep(0.3)
        self._key_down("a")
        self.sleep(5)
        self._key_up("a")
        self.sleep(0.3)
        self._key_down("s")
        self.sleep(1.5)
        self._key_up("s")
        self.sleep(0.3)
        self._key_down("d")
        self.sleep(2.9)
        self._key_up("d")
        self.sleep(0.3)
        self._key_down("s")
        self.sleep(2)
        self._key_up("s")
        self.sleep(0.4)
        self._key_down("w")
        self.sleep(2)
        self._key_up("w")

        self._tap_key("4")
        self.sleep(0.3)
        self._key_down("s")
        self.sleep(0.2)
        self._key_up("s")
        self.sleep(2)

        self.log_info("等待 G 层战斗2")
        self._fight_until_no_monster(
            timeout_no_monster=10,
            wait_for_monster=True,
            role_to_switch_back="3",
            loot=True,
            attack_cycles=3,
        )

        self._key_down("w")
        self.sleep(3)
        self._key_up("w")
        self.sleep(0.3)

        self._key_down("d")
        self.sleep(2)
        self._key_down("s")
        self.sleep(3)
        self._key_up("s")
        self.sleep(0.3)
        self._key_up("d")

        self.sleep(0.3)
        self._key_down("a")
        self.sleep(1.3)
        self._key_up("a")
        self.sleep(0.3)

        self._key_down("s")
        self._tap_repeat("f", 7, 0.1)
        self._key_up("s")
        self.sleep(0.3)

        self._key_down("d")
        self._tap_repeat("f", 15, 0.1)
        self._key_up("d")
        self.sleep(0.3)

        self._key_down("a")
        self._tap_repeat("f", 22, 0.1)
        self._key_up("a")
        self.sleep(0.3)

        self._key_down("d")
        self.sleep(1.6)
        self._key_up("d")
        self.sleep(0.2)
        self._key_down("s")
        self.sleep(6)
        self._key_up("s")
        self.sleep(0.3)
        self._key_down("a")
        self.sleep(3)
        self._key_up("a")
        self.sleep(0.3)

        self._tap_key("f")
        self.sleep(1)
        self._key_down("d")
        self.sleep(0.3)
        self._key_up("d")
        self.sleep(0.2)
        self._key_down("s")
        self.sleep(1.5)
        self._key_up("s")

        self._tap_key("f")
        self.sleep(1)
        self._key_down("w")
        self.sleep(1.5)
        self._key_up("w")
        self.sleep(0.1)
        self._key_down("a")
        self.sleep(2.3)
        self._key_up("a")
        self.sleep(0.2)

        self._key_down("w")
        self._tap_repeat("f", 19, 0.2)
        self._key_up("w")
        self.sleep(0.3)
        self._key_down("s")
        self.sleep(0.5)
        self._key_up("s")

        return True

    def _enter_heist(self) -> bool:
        self.log_info("检测小吱交互")
        if not self._wait_text("小吱", (800, 380, 35, 25), timeout=8):
            return False

        self._tap_key("f")
        self.sleep(0.8)

        if not self._click_text("我要参加", (910, 325, 70, 25), timeout=10):
            return False

        self.sleep(2)
        self.operate_click(890 / 1280, 320 / 720)

        if not self._click_text("进入", (900, 620, 170, 35), timeout=60):
            return False

        self.log_info("等待进入地图")
        return self._wait_text("本局收益", (30, 250, 100, 20), timeout=90)

    def _evacuate_once(self) -> bool:
        self._tap_key("f")
        self.sleep(1.5)
        if not self._click_text("确认撤离", (710, 490, 120, 30), timeout=15):
            return False
        self.sleep(10)
        return True

    def _switch_role(self, key: str, repeat=1, delay=0.2):
        for _ in range(repeat):
            self._tap_key(key)
            self.sleep(delay)

    def _tap_repeat(self, key: str, repeat: int, delay: float):
        for _ in range(repeat):
            self._tap_key(key)
            self.sleep(delay)

    def _tap_key(self, key: str):
        self.send_key(key)

    def _key_down(self, key: str):
        interaction = getattr(self.executor, "interaction", None)
        if interaction is not None and hasattr(interaction, "key_down"):
            interaction.key_down(key)
            return
        self.send_key_down(key)

    def _key_up(self, key: str):
        interaction = getattr(self.executor, "interaction", None)
        if interaction is not None and hasattr(interaction, "key_up"):
            interaction.key_up(key)
            return
        self.send_key_up(key)

    def _fight_until_no_monster(
        self,
        timeout_no_monster=10,
        wait_for_monster=True,
        role_to_switch_back=None,
        loot=False,
        attack_cycles=3,
    ) -> bool:
        if wait_for_monster and not self._wait_monster(timeout_no_monster):
            return False

        no_monster_start = None
        while True:
            if self._check_monster():
                no_monster_start = None
                self._attack_cycle(times=attack_cycles, loot=loot)
            else:
                now = time.monotonic()
                if no_monster_start is None:
                    no_monster_start = now
                elif now - no_monster_start >= timeout_no_monster:
                    break
                self.sleep(0.05)

        if role_to_switch_back:
            self._switch_role(role_to_switch_back, repeat=3, delay=0.2)
        return True

    def _wait_monster(self, timeout=6) -> bool:
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            if self._check_monster():
                return True
            self.sleep(0.2)
        return False

    def _attack_cycle(self, times=3, loot=False):
        for _ in range(times):
            self._tap_key("space")
            self.click(x=0.5, y=0.5)
            self.sleep(0.25)
        if loot:
            self._tap_key("f")

    def _check_monster(self) -> bool:
        frame = self.frame
        if frame is None:
            return False

        h, w = frame.shape[:2]
        x, y, rw, rh = self._scale_roi(33, 27, 1222, 639, w, h)
        crop = frame[y : y + rh, x : x + rw]
        if crop.size == 0:
            return False

        target_a = np.array([243, 32, 33], dtype=np.uint8)
        target_b = np.array([33, 32, 243], dtype=np.uint8)
        tol = np.array([8, 8, 8], dtype=np.uint8)

        lower_a = np.maximum(target_a - tol, 0)
        upper_a = np.minimum(target_a + tol, 255)
        lower_b = np.maximum(target_b - tol, 0)
        upper_b = np.minimum(target_b + tol, 255)

        mask_a = cv2.inRange(crop, lower_a, upper_a)
        mask_b = cv2.inRange(crop, lower_b, upper_b)
        mask = cv2.bitwise_or(mask_a, mask_b)
        return cv2.countNonZero(mask) >= 3

    def _wait_text(self, expected: str, roi_720: tuple[int, int, int, int], timeout=10) -> bool:
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            if self._find_text(expected, roi_720) is not None:
                return True
            self.sleep(0.2)
        return False

    def _click_text(self, expected: str, roi_720: tuple[int, int, int, int], timeout=10) -> bool:
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            box = self._find_text(expected, roi_720)
            if box is not None:
                self.operate_click(box)
                return True
            self.sleep(0.2)
        return False

    def _find_text(self, expected: str, roi_720: tuple[int, int, int, int]):
        roi_box = self._roi_box(*roi_720)
        words = self.ocr(box=roi_box, match=expected)
        if words:
            return words[0]
        return None

    def _roi_box(self, x: int, y: int, w: int, h: int):
        return self.box_of_screen(
            x / self.BASE_WIDTH,
            y / self.BASE_HEIGHT,
            (x + w) / self.BASE_WIDTH,
            (y + h) / self.BASE_HEIGHT,
        )

    def _scale_roi(self, x: int, y: int, w: int, h: int, fw: int, fh: int):
        sx = max(0, min(fw - 1, int(round(x * fw / self.BASE_WIDTH))))
        sy = max(0, min(fh - 1, int(round(y * fh / self.BASE_HEIGHT))))
        ex = max(sx + 1, min(fw, int(round((x + w) * fw / self.BASE_WIDTH))))
        ey = max(sy + 1, min(fh, int(round((y + h) * fh / self.BASE_HEIGHT))))
        return sx, sy, ex - sx, ey - sy

    def _exit_to_main(self):
        for _ in range(3):
            self._tap_key("esc")
            self.sleep(1)
        self.sleep(1.5)
        self.operate_click(775 / 1280, 473 / 720)
        self.sleep(0.5)
        self.operate_click(775 / 1280, 473 / 720)
        self.sleep(10)
