"""Katalog ile manifestlerin tutarlılığı. Yalnızca standart kitaplık."""
import json
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent


def yukle(yol):
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


class KatalogTesti(unittest.TestCase):
    def setUp(self):
        self.katalog = yukle(KOK / "katalog.json")

    def test_katalog_alanlari(self):
        self.assertIn("surum", self.katalog)
        self.assertIsInstance(self.katalog["paketler"], list)
        self.assertTrue(self.katalog["paketler"])

    def test_idler_benzersiz(self):
        idler = [p["id"] for p in self.katalog["paketler"]]
        self.assertEqual(len(idler), len(set(idler)))

    def test_manifestler_var_ve_okunur(self):
        for p in self.katalog["paketler"]:
            with self.subTest(paket=p["id"]):
                yol = KOK / p["manifest"]
                self.assertTrue(yol.is_file(), f"manifest yok: {p['manifest']}")
                self.assertIsInstance(yukle(yol), dict)

    def test_her_manifest_katalogda(self):
        katalogdakiler = {p["manifest"] for p in self.katalog["paketler"]}
        for yol in (KOK / "paketler").glob("*/manifest.json"):
            with self.subTest(manifest=yol.parent.name):
                self.assertIn(yol.relative_to(KOK).as_posix(), katalogdakiler)


if __name__ == "__main__":
    unittest.main()
