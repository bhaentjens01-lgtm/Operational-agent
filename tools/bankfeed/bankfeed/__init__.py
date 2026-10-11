"""Bankfeed — read-only koppeling van privérekeningen via Enable Banking (PSD2 AIS).

Enkel leestoegang: deze module implementeert bewust geen betalingsendpoints.
Geen bankdata, sleutels of IBAN's in git: alles komt uit omgevingsvariabelen
en wordt weggeschreven naar een lokale datamap (gitignored) of een privé Google Sheet.
"""

__version__ = "0.1.0"
