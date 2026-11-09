import unittest
import numpy as np
from main import Tracker, PeopleDetector, suppress


class TrackerTests(unittest.TestCase):
    def test_same_person_counted_once(self):
        t=Tracker()
        for i in range(20):
            t.update([[100+i,20,64,140]],i/10)
        self.assertEqual(t.total,1)

    def test_two_people(self):
        t=Tracker()
        for i in range(5):
            t.update([[10,10,64,140],[400,10,64,140]],i/10)
        self.assertEqual(t.total,2)

    def test_brief_occlusion_preserves_count(self):
        t=Tracker()
        for i in range(3):
            t.update([[100,10,64,140]],i/10)
        t.update([],0.3)
        t.update([[100,10,64,140]],0.8)
        self.assertEqual(t.total,1)
        self.assertEqual(len(t.tracks),1)

    def test_unconfirmed_detection_not_counted(self):
        t=Tracker()
        t.update([[100,10,64,140]],0)
        t.update([],0.1)
        t.update([[100,10,64,140]],0.2)
        self.assertEqual(t.total,0)

    def test_return_after_expiry_is_new_id(self):
        t=Tracker(confirmations=1, max_gap=2.0)
        t.update([[100,10,64,140]],0)
        t.update([[100,10,64,140]],3)
        self.assertEqual(t.total,2)
        t.reset()
        self.assertEqual(t.total,0)
        self.assertFalse(t.tracks)

    def test_duplicate_boxes_suppressed(self):
        self.assertEqual(len(suppress([[0,0,64,128],[1,1,64,128]],[1,2])),1)

    def test_intermittent_detections_can_confirm(self):
        t=Tracker()
        for i in range(5):
            t.update([[100,10,64,140]] if i % 2 == 0 else [],i/10)
        self.assertEqual(t.total,1)

    def test_overlapping_people_kept_at_new_threshold(self):
        boxes=[[0,0,64,128],[20,0,64,128]]
        self.assertEqual(len(suppress(boxes,[2,1],0.65)),2)

    def test_blank_and_small_frames(self):
        d=PeopleDetector()
        self.assertEqual(len(d.detect(np.zeros((360,640,3),np.uint8))),0)
        self.assertEqual(d.detect(np.zeros((30,30,3),np.uint8)),[])


if __name__=='__main__':
    unittest.main()
