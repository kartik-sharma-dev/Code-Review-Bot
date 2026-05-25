import streamlit as st
from reviewer import review_code

st.set_page_config(page_title="Code Review Bot", page_icon="🤖", layout="wide")

st.title("🤖 Code Review Bot")
st.caption("Powered by CodeBERT — paste your code and get instant quality scores.")

code = st.text_area(
    "Your Code",
    height=300,
    placeholder="Paste your code here...",
)

if st.button("Review Code", type="primary", disabled=not code.strip()):
    with st.spinner("Analyzing..."):
        scores = review_code(code)

    st.divider()
    st.subheader("Review Scores")

    col1, col2, col3, col4 = st.columns(4)

    def score_color(value, invert=False):
        if invert:
            value = 10 - value
        if value >= 7:
            return "normal"
        elif value >= 4:
            return "off"
        return "inverse"

    col1.metric("Quality", f"{scores['quality']:.1f} / 10",
                delta="good" if scores["quality"] >= 7 else "needs work",
                delta_color=score_color(scores["quality"]))

    col2.metric("Bug Risk", f"{scores['bug_risk']:.1f} / 10",
                delta="low risk" if scores["bug_risk"] <= 4 else "high risk",
                delta_color=score_color(scores["bug_risk"], invert=True))

    col3.metric("Readability", f"{scores['readability']:.1f} / 10",
                delta="good" if scores["readability"] >= 7 else "needs work",
                delta_color=score_color(scores["readability"]))

    col4.metric("Complexity", f"{scores['complexity']:.1f} / 10",
                delta="simple" if scores["complexity"] <= 4 else "complex",
                delta_color=score_color(scores["complexity"], invert=True))

    st.divider()
    st.subheader("Score Breakdown")
    for label, key, invert in [
        ("Quality", "quality", False),
        ("Bug Risk (lower is better)", "bug_risk", True),
        ("Readability", "readability", False),
        ("Complexity (lower is better)", "complexity", True),
    ]:
        val = scores[key]
        display_val = (10 - val) if invert else val
        st.write(f"**{label}**: {val:.1f}")
        st.progress(display_val / 10)
