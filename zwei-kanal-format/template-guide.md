# Template: guide in the Two-Channel Format (application 2)

Copy the content of the block into a new file (for example `README.md`) and replace all `<…>`. A note after `←` names the
condition for a field or a line: delete it if the condition does not apply, and always delete the note. BLOCK B stays
German (operator 25.11.2026 21:40); its placeholders are German. Example: `example-guide.md`.

````markdown
# <Name> <version>

## BLOCK A – order to the AI that sets it up

```text
PURPOSE:      <What stands at the end, in one to three sentences, checkable.>
APPLIES TO:   <What the guide is meant for.>
DOES NOT APPLY TO: <What it is not meant for, and where that is described instead.>
PREREQUISITES: <Language and version, access, services that must be there beforehand.>
FILES:        <file> (<what for>) · <file> (<what for>) · …
TERMS:        <term> = <exact meaning, as the steps use it>.   ← if a term allows several readings
BEHAVIOUR:    <How the tool behaves today, one checkable statement per function.>   ← for tools that run
```

### STEPS (in this order; every step has a checkable result)

1. **<Short name>.** <What exactly to do: which file, which place, which value.>
   *Result:* <Command or observation that shows the step succeeded.>
2. **<Short name>.** <…> Where something is to be inserted:

   | Placeholder | insert |
   |---|---|
   | `<…>` | <Source of the value>. If the order names no value, then the default <value> applies; name it in the delivery as open. |
   | `<…>` | <Source of the value>. If the value is missing, then it stays open and the step waits.   ← for addressees, publication, deletion and credentials; there is never a default for them |

   *Result:* <…>

```text
CHECK:        <What is confirmed at the end: one command, or the results of the steps that apply together.>
FAIL-MODE:    <If a step does not work, then …. If only a detail is missing, then ….>
DO NOT:       <For each limit first what is right, then what the AI leaves.>   ← if there are limits that no step names
DELIVERY:     <files created and changed> · <result of each check> · open items ·
              every place where this guide was not enough, with quote.
REFERENCE:    <Where details are.>   ← if needed
```

---

## BLOCK B – für Menschen

<Ein echter Vorfall oder ein Beispiel, das zeigt, welches Problem das hier löst.>

<Was es tut – so lang, wie ein Mensch zum Verstehen braucht, und kürzer als Block A.>

## Was du im Alltag tust

<Was der Mensch selbst tut, wenn es läuft, und woran er erkennt, ob es geklappt hat.>
````
