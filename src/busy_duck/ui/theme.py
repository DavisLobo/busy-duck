LIGHT_THEME = """
QMainWindow, QWidget {
    background: #F1F5F6;
    color: #24323A;
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
}

#sidebar {
    background: #E7EFF0;
    border-right: 1px solid #D6E1E3;
}

#logo {
    color: #173F46;
    font-size: 21px;
    font-weight: 800;
}

#tagline, #pageSubtitle, #statusLabel {
    color: #6B7D83;
}

#navButton {
    background: transparent;
    color: #52666D;
    border: none;
    border-radius: 8px;
    padding: 11px;
    text-align: left;
}

#navButton:enabled,
#navButton:hover {
    background: #D4E8E6;
    color: #173F46;
    font-weight: 700;
}

#sectionTitle, #metricLabel {
    color: #789096;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
}

#providerLabel, #localStorage {
    color: #52666D;
}

#localStorage {
    font-size: 11px;
}

#pageTitle, #sectionHeading {
    color: #173F46;
    font-weight: 800;
}

#pageTitle {
    font-size: 28px;
}

#sectionHeading {
    font-size: 18px;
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

#primaryButton:disabled {
    background: #9BC8C2;
}

QLineEdit, QDateEdit, QComboBox {
    background: #FFFFFF;
    color: #24323A;
    border: 1px solid #D2DEE0;
    border-radius: 7px;
    padding: 8px;
}

QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
    border: 1px solid #2A9D8F;
}

#metricCard, #detailCard {
    background: #FFFFFF;
    border: 1px solid #DCE6E8;
    border-radius: 12px;
}

#metricValue {
    color: #173F46;
    font-size: 25px;
    font-weight: 800;
}

QTableView {
    background: #FFFFFF;
    color: #24323A;
    border: 1px solid #DCE6E8;
    border-radius: 10px;
    gridline-color: #EDF2F3;
    selection-background-color: #D4E8E6;
    selection-color: #173F46;
    alternate-background-color: #F8FAFA;
}

QHeaderView::section {
    background: #EAF1F2;
    color: #60747A;
    border: none;
    border-bottom: 1px solid #DCE6E8;
    padding: 12px 8px;
    font-weight: 800;
}

QScrollBar:vertical {
    background: #E7EFF0;
    width: 10px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background: #B7CCCF;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}
"""

DARK_THEME = """
QMainWindow, QWidget {
    background: #101A20;
    color: #E6EEF0;
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
}

#sidebar {
    background: #14262C;
    border-right: 1px solid #253E45;
}

#logo {
    color: #F4B942;
    font-size: 21px;
    font-weight: 800;
}

#tagline, #pageSubtitle, #statusLabel {
    color: #9AAEB3;
}

#navButton {
    background: transparent;
    color: #A9BBC0;
    border: none;
    border-radius: 8px;
    padding: 11px;
    text-align: left;
}

#navButton:enabled,
#navButton:hover {
    background: #214148;
    color: #F3FAFA;
    font-weight: 700;
}

#sectionTitle, #metricLabel {
    color: #82999F;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
}

#providerLabel, #localStorage {
    color: #A9BBC0;
}

#localStorage {
    font-size: 11px;
}

#pageTitle, #sectionHeading {
    color: #F1F7F8;
    font-weight: 800;
}

#pageTitle {
    font-size: 28px;
}

#sectionHeading {
    font-size: 18px;
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
    background: #35B3A4;
}

#primaryButton:disabled {
    background: #356C68;
}

QLineEdit, QDateEdit, QComboBox {
    background: #182A31;
    color: #E6EEF0;
    border: 1px solid #304950;
    border-radius: 7px;
    padding: 8px;
}

QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
    border: 1px solid #35B3A4;
}

#metricCard, #detailCard, QTableView {
    background: #182A31;
    border: 1px solid #304950;
    border-radius: 12px;
}

#metricValue {
    color: #F1F7F8;
    font-size: 25px;
    font-weight: 800;
}

QTableView {
    gridline-color: #253E45;
    selection-background-color: #245B59;
    selection-color: #FFFFFF;
    alternate-background-color: #1B3037;
}

QHeaderView::section {
    background: #1D343B;
    color: #A9BBC0;
    border: none;
    border-bottom: 1px solid #304950;
    padding: 12px 8px;
    font-weight: 800;
}

QScrollBar:vertical {
    background: #14262C;
    width: 10px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background: #3B5D63;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}
"""