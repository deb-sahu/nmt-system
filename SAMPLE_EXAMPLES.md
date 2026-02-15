# Example Inputs

Here are some medical text examples to try in the app. The default model translates English to German.

---

## Basic Test

**Source:**
```
The patient has fever.
```

**Reference:**
```
Der Patient hat Fieber.
```

---

## Medical Sentence

**Source:**
```
The patient presented with fever and cough. Blood pressure was elevated.
```

**Reference:**
```
Der Patient präsentierte sich mit Fieber und Husten. Der Blutdruck war erhöht.
```

---

## Clinical Note

**Source:**
```
The patient is a 65-year-old male with a history of diabetes and hypertension. He reports chest pain and shortness of breath. Vital signs are stable.
```

**Reference:**
```
Der Patient ist ein 65-jähriger Mann mit Vorgeschichte von Diabetes und Bluthochdruck. Er berichtet über Brustschmerzen und Atemnot. Die Vitalzeichen sind stabil.
```

---

## Medication Instructions

**Source:**
```
Take one tablet twice daily with food. Do not exceed the recommended dose. Contact your doctor if symptoms persist.
```

**Reference:**
```
Nehmen Sie zweimal täglich eine Tablette zu den Mahlzeiten ein. Überschreiten Sie nicht die empfohlene Dosis. Kontaktieren Sie Ihren Arzt, wenn die Symptome anhalten.
```

---

## Spanish (switch model to opus-mt-en-es)

**Source:**
```
The patient has a headache and nausea. No allergies reported.
```

**Reference:**
```
El paciente tiene dolor de cabeza y náuseas. No se reportaron alergias.
```

---

## Multiple References

You can paste multiple references (one per line) to give BLEU more options to match against.

**Source:**
```
Discontinue the medication if rash or swelling occurs.
```

**References (paste both lines):**
```
Setzen Sie das Medikament ab, wenn Hautausschlag oder Schwellung auftreten.
Brechen Sie die Medikamenteneinnahme ab, wenn ein Ausschlag oder eine Schwellung auftritt.
```

---

## Tips

- Click Translate first, then add the reference to see BLEU
- Paste extra translations in "Add more candidates" to compare scores
- For file upload, put references in a .txt file (one per line)
