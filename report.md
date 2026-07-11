# Django Transactions, ORM, and SQLAlchemy Comparison — Summary

## 1. How Django `save()` works

- `model.save()` immediately executes SQL (`INSERT` or `UPDATE`)
- It does **not track changes over time**
- Django ORM has **no Unit of Work pattern**

Key idea:
> Django does not delay database writes — it executes them immediately.

---

## 2. What `transaction.atomic()` does in Django

- Creates a database transaction boundary
- Groups multiple SQL statements into one atomic unit

Behavior:

### Inside `atomic()`:
- SQL is executed immediately when `save()` is called
- Changes are **not permanently saved yet**
- Commit happens only when the block successfully exits

### If an exception occurs:
- Entire transaction is rolled back
- All executed SQL statements are undone

---

## 3. Important misconception clarified

❌ Wrong:
- “Transaction delays `save()` until commit”

✅ Correct:
- `save()` always executes SQL immediately
- Transaction only controls whether those SQL changes are committed or rolled back

---

## 4. `commit=False` in ModelForms

- Prevents `form.save()` from writing to DB
- Returns an **unsaved model instance**

Used when:
- You need to modify the instance before saving
- You need to set fields not provided by the form (e.g. foreign keys like `user`)

Example:

```python
obj = form.save(commit=False)
obj.user = request.user
obj.save()