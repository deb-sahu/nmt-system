# Sample Examples for the NMT App

Copy-paste these into the app to try translation and BLEU evaluation. The default model is **English → German** (Helsinki-NLP/opus-mt-en-de).

---

## Example 1: Short medical sentence (en → de)

**Source text** (paste in "Source text" box):
```
The patient presented with fever and cough. Blood pressure was elevated.
```

**Reference translation** (paste in "Reference translation" box for BLEU):
```
Der Patient präsentierte sich mit Fieber und Husten. Der Blutdruck war erhöht.
```

---

## Example 2: Clinical note (en → de)

**Source text:**
```
The patient is a 65-year-old male with a history of diabetes and hypertension. He reports chest pain and shortness of breath. Vital signs are stable.
```

**Reference translation:**
```
Der Patient ist ein 65-jähriger Mann mit Vorgeschichte von Diabetes und Bluthochdruck. Er berichtet über Brustschmerzen und Atemnot. Die Vitalzeichen sind stabil.
```

---

## Example 3: Medication instruction (en → de)

**Source text:**
```
Take one tablet twice daily with food. Do not exceed the recommended dose. Contact your doctor if symptoms persist.
```

**Reference translation:**
```
Nehmen Sie zweimal täglich eine Tablette zu den Mahlzeiten ein. Überschreiten Sie nicht die empfohlene Dosis. Kontaktieren Sie Ihren Arzt, wenn die Symptome anhalten.
```

---

## Example 4: Use with Spanish model (en → es)

Switch the **model** in the sidebar to **Helsinki-NLP/opus-mt-en-es**, then use:

**Source text:**
```
The patient has a headache and nausea. No allergies reported.
```

**Reference translation:**
```
El paciente tiene dolor de cabeza y náuseas. No se reportaron alergias.
```

---

## Example 5: Multiple references (for better BLEU)

You can paste **multiple references** (one per line). BLEU will use the best-matching length for brevity penalty and max counts for n-grams.

**Source text:**
```
Discontinue the medication if rash or swelling occurs.
```

**Reference 1:**
```
Setzen Sie das Medikament ab, wenn Hautausschlag oder Schwellung auftreten.
```

**Reference 2:**
```
Brechen Sie die Medikamenteneinnahme ab, wenn ein Ausschlag oder eine Schwellung auftritt.
```

Paste both lines in the reference box (one per line).

---

## Quick test (minimal)

**Source:**
```
The patient has fever.
```

**Reference (German):**
```
Der Patient hat Fieber.
```

---

## Tips

- Click **Translate** first, then add the reference and you’ll see BLEU, brevity penalty, and the n-gram table.
- To compare **multiple candidates**: paste another translation in “Add more candidates” (one per line) to see different BLEU scores.
- For **file upload**: put the reference(s) in a `.txt` file, one reference per line, and use “Upload file” in the reference section.
