from changed_directory import ChangedDirectory

# Test Cases: data/minimal project fixture


def test_approved_with_high_powered_approval(changed_file_y):
    approvals = ("B", )
    changed_dir = ChangedDirectory(changed_file_y, approvals)
    assert changed_dir.approved


def test_approved_with_low_powered_approvals(changed_file_y):
    approvals = ("A", "C")
    changed_dir = ChangedDirectory(changed_file_y, approvals)
    assert changed_dir.approved


def test_approved_with_insufficient_approvals(changed_file_y):
    approvals = ("D", )
    changed_dir = ChangedDirectory(changed_file_y, approvals)
    assert not changed_dir.approved


# Test Cases: data/repo project fixture


def test_approved_1a(changed_file_follow):
    """
    Check parent directories for approval
    """
    approvals = ("alovelace", "ghopper")
    changed_dir = ChangedDirectory(changed_file_follow, approvals)
    assert changed_dir.approved is True


def test_approved_1b(changed_file_user):
    approvals = ("alovelace", "ghopper")
    changed_dir = ChangedDirectory(changed_file_user, approvals)
    assert changed_dir.approved is True


def test_approved_2(changed_file_follow):
    approvals = ("alovelace", )
    changed_dir = ChangedDirectory(changed_file_follow, approvals)
    assert changed_dir.approved is False


def test_approved_3(changed_file_follow):
    approvals = ("eclarke", )
    changed_dir = ChangedDirectory(changed_file_follow, approvals)
    assert changed_dir.approved is False


def test_approved_4(changed_file_follow):
    approvals = ("alovelace", "eclarke")
    changed_dir = ChangedDirectory(changed_file_follow, approvals)
    assert changed_dir.approved is True


def test_approved_5(changed_file_tweet):
    approvals = ("mfox", )
    changed_dir = ChangedDirectory(changed_file_tweet, approvals)
    assert changed_dir.approved is True
