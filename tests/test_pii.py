from app.pii import hash_user_id, scrub_text, summarize_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_phone_vn() -> None:
    out = scrub_text("Call 0901234567 for help")
    assert "0901234567" not in out
    assert "REDACTED_PHONE_VN" in out


def test_scrub_phone_vn_plus84() -> None:
    out = scrub_text("Phone: +84901234567")
    assert "+84901234567" not in out
    assert "REDACTED_PHONE_VN" in out


def test_scrub_credit_card() -> None:
    out = scrub_text("Card number 4111 1111 1111 1111")
    assert "4111" not in out
    assert "REDACTED_CREDIT_CARD" in out


def test_scrub_credit_card_no_spaces() -> None:
    out = scrub_text("Card 4111111111111111 was charged")
    assert "4111111111111111" not in out
    assert "REDACTED_CREDIT_CARD" in out


def test_scrub_passport() -> None:
    out = scrub_text("Passport A1234567 holder")
    assert "A1234567" not in out
    assert "REDACTED_PASSPORT" in out


def test_scrub_multiple_pii() -> None:
    text = "Email buyer@shop.com, phone 0912345678"
    out = scrub_text(text)
    assert "buyer@" not in out
    assert "0912345678" not in out


def test_scrub_no_pii() -> None:
    text = "What is your refund policy?"
    assert scrub_text(text) == text


def test_summarize_truncates() -> None:
    long_text = "A" * 200
    out = summarize_text(long_text, max_len=80)
    assert len(out) == 83  # 80 chars + "..."
    assert out.endswith("...")


def test_summarize_short_text() -> None:
    out = summarize_text("Hello")
    assert out == "Hello"
    assert "..." not in out


def test_summarize_scrubs_pii() -> None:
    out = summarize_text("Contact me at test@example.com")
    assert "test@" not in out
    assert "REDACTED_EMAIL" in out


def test_hash_user_id_deterministic() -> None:
    h1 = hash_user_id("user123")
    h2 = hash_user_id("user123")
    assert h1 == h2
    assert len(h1) == 12


def test_hash_user_id_different_inputs() -> None:
    h1 = hash_user_id("user_a")
    h2 = hash_user_id("user_b")
    assert h1 != h2
