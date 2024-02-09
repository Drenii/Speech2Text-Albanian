from g2p_en import G2p

# Convert text to IPA symbols
text = "Tungjatjeta! Si jeni?"
g2p = G2p()
pronunciations = g2p(text)

ipa = ' '.join(pronunciations)

print(ipa)
