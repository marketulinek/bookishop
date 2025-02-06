## Pre-commit Hook for Model Changes

To ensure that database diagrams stay up to date, I've added a **Git pre-commit hook** that runs before each commit.

If you modify `models.py` in any app, the hook will remind you to update the corresponding Mermaid class diagram.

### 📌 Setting Up the Pre-commit Hook
Run the following command **once** to install it:

```
cp scripts/pre-commit .git/hooks/pre-commit
```
```
chmod +x .git/hooks/pre-commit
```
