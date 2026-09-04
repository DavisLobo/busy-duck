LIGHT_THEME = """
QMainWindow, QWidget {
    background: #F4F7F9;
    color: #172033;
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
}

#sidebar {
    background: #102A43;
}

#logo {
    color: #F4B942;
    font-size: 21px;
    font-weight: 800;
}

#tagline, #pageSubtitle, #statusLabel {
    color: #718096;
}

#sidebar #tagline, #sidebar #statusLabel {
    color: #AFC2D4;
}

#navButton {
    background: transparent;
    color: #C8D5E1;
    border: none;
    border-radius: 8px;
    padding: 11px;
    text-align: left;
}

#navButton:checked, #navButton:hover {
    background: #21415C;
    color: white;
}

#primaryButton {
    background: #2A9D8F;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 17px;
    font-weight: 700;
}

#primaryButton:hover {
    background: #238276;
}

#pageTitle {
    color: #102A43;
    font-size: 28px;
    font-weight: 800;
}

#sectionHeading {
    color: #102A43;
    font-size: 18px;
    font-weight: 800;
}

#metricCard, #detailCard {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

#metricLabel, #sectionTitle {
    color: #718096;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
}

#metricValue {
    color: #102A43;
    font-size: 25px;
    font-weight: 800;
}

QLineEdit, QDateEdit, QComboBox {
    background: white;
    color: #172033;
    border: 1px solid #D8E0E8;
    border-radius: 7px;
    padding: 8px;
}

QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
    border: 1px solid #2A9D8F;
}

QTableView {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    gridline-color: #EDF2F7;
    selection-background-color: #D9F0EC;
    selection-color: #102A43;
}

QHeaderView::section {
    background: #F8FAFC;
    color: #718096;
    border: none;
    padding: 12px 8px;
    font-weight: 800;
}
"""

DARK_THEME = """
QMainWindow, QWidget {
    background: #101820;
    color: #E6EDF3;
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
}

#sidebar {
    background: #08141F;
}

#logo {
    color: #F4B942;
    font-size: 21px;
    font-weight: 800;
}

#tagline, #pageSubtitle, #statusLabel {
    color: #91A4B5;
}

#navButton {
    background: transparent;
    color: #AFC2D4;
    border: none;
    border-radius: 8px;
    padding: 11px;
    text-align: left;
}

#navButton:checked, #navButton:hover {
    background: #18354B;
    color: white;
}

#primaryButton {
    background: #2A9D8F;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 17px;
    font-weight: 700;
}

#pageTitle, #sectionHeading {
    color: #F1F5F9;
    font-weight: 800;
}

#pageTitle {
    font-size: 28px;
}

#sectionHeading {
    font-size: 18px;
}

#metricCard, #detailCard, QTableView {
    background: #172532;
    border: 1px solid #294052;
    border-radius: 12px;
}

#metricLabel, #sectionTitle {
    color: #91A4B5;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
}

#metricValue {
    color: #F1F5F9;
    font-size: 25px;
    font-weight: 800;
}

QLineEdit, QDateEdit, QComboBox {
    background: #172532;
    color: #E6EDF3;
    border: 1px solid #294052;
    border-radius: 7px;
    padding: 8px;
}

QTableView {
    gridline-color: #294052;
    selection-background-color: #245B59;
    selection-color: white;
}

QHeaderView::section {
    background: #1D303F;
    color: #AFC2D4;
    border: none;
    padding: 12px 8px;
    font-weight: 800;
}
"""