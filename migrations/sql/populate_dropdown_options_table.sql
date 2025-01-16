-- Real Estate Property Monthly Cashflow
INSERT INTO dropdown_options (dropdown_name, value, label, order_index, is_active) VALUES
('real_estate_property_monthly_cashflow', 'Rental Income', 'Rental Income', 1, 1),
('real_estate_property_monthly_cashflow', 'Parking Fees', 'Parking Fees', 2, 1),
('real_estate_property_monthly_cashflow', 'Storage Unit Fees', 'Storage Unit Fees', 3, 1),
('real_estate_property_monthly_cashflow', 'Laundry Machine', 'Laundry Machine', 4, 1),
('real_estate_property_monthly_cashflow', 'AirBnB', 'AirBnB', 5, 1),
('real_estate_property_monthly_cashflow', 'Utilities Income', 'Utilities Income', 6, 1),
('real_estate_property_monthly_cashflow', 'Vending Machine', 'Vending Machine', 7, 1);

-- Real Estate Property Expenses
INSERT INTO dropdown_options (dropdown_name, value, label, order_index, is_active) VALUES
('real_estate_property_monthly_expenses', 'Property Tax', 'Property Tax', 1, 1),
('real_estate_property_monthly_expenses', 'Property Insurance', 'Property Insurance', 2, 1),
('real_estate_property_monthly_expenses', 'Lawn Care', 'Lawn Care', 3, 1),
('real_estate_property_monthly_expenses', 'Property Management', 'Property Management', 4, 1),
('real_estate_property_monthly_expenses', 'HOA/Condo Fees', 'HOA/Condo Fees', 5, 1),
('real_estate_property_monthly_expenses', 'Maintenance and Repairs', 'Maintenance and Repairs', 6, 1),
('real_estate_property_monthly_expenses', 'Utilities Expenses', 'Utilities Expenses', 7, 1),
('real_estate_property_monthly_expenses', 'Vacancy Reserve', 'Vacancy Reserve', 8, 1),
('real_estate_property_monthly_expenses', 'Capital Expenditure Reserve', 'Capital Expenditure Reserve', 9, 1),
('real_estate_property_monthly_expenses', 'Advertising and Marketing', 'Advertising and Marketing', 10, 1),
('real_estate_property_monthly_expenses', 'Rental Incentives', 'Rental Incentives', 11, 1),
('real_estate_property_monthly_expenses', 'Legal and Accounting', 'Legal and Accounting', 12, 1);

-- Real Estate Property Capital Investments
INSERT INTO dropdown_options (dropdown_name, value, label, order_index, is_active) VALUES
('real_estate_property_capital_investments', 'Down Payment', 'Down Payment, 1, 1),
('real_estate_property_capital_investments', 'Closing Costs', 'Closing Costs', 2, 1),
('real_estate_property_capital_investments', 'Before Closing Insurance', 'Before Closing Insurance', 3, 1),
('real_estate_property_capital_investments', 'Initial Property Tax', 'Initial Property Tax', 4, 1),
('real_estate_property_capital_investments', 'Renovation and Improvement Costs', 'Renovation and Improvement Costs', 5, 1),
('real_estate_property_capital_investments', 'Furnishing and Fixtures', 'Furnishing and Fixtures', 6, 1),
('real_estate_property_capital_investments', 'Landscaping and Exterior', 'Landscaping and Exterior', 7, 1),
('real_estate_property_capital_investments', 'Property Management Setup Costs', 'Property Management Setup Costs', 8, 1),
('real_estate_property_capital_investments', 'Legal or Zoning Adjustment', 'Legal or Zoning Adjustment', 9, 1),
('real_estate_property_capital_investments', 'Development or Permit Fees', 'Development or Permit Fees', 10, 1),
('real_estate_property_capital_investments', 'Mortgage Points', 'Mortgage Points', 11, 1),
('real_estate_property_capital_investments', 'Utility Hookups', 'Utility Hookups', 12, 1),
('real_estate_property_capital_investments', 'Repair after Closing', 'Repair after Closing', 13, 1);

-- Priorities
INSERT INTO dropdown_options (dropdown_name, value, label, order_index, is_active) VALUES
('priorities', 'high', 'High Priority', 1, 1),
('priorities', 'medium', 'Medium Priority', 2, 1),
('priorities', 'low', 'Low Priority', 3, 1);

-- Document Types
INSERT INTO dropdown_options (dropdown_name, value, label, order_index, is_active) VALUES
('document_types', 'pdf', 'PDF Document', 1, 1),
('document_types', 'doc', 'Word Document', 2, 1),
('document_types', 'xls', 'Excel Spreadsheet', 3, 1),
('document_types', 'img', 'Image File', 4, 1);

-- Gender
INSERT INTO dropdown_options (dropdown_name, value, label, order_index, is_active) VALUES
('gender', 'M', 'Male', 1, 1),
('gender', 'F', 'Female', 2, 1),
('gender', 'O', 'Other', 3, 1);

-- Yes/No
INSERT INTO dropdown_options (dropdown_name, value, label, order_index, is_active) VALUES
('yes_no', 'Y', 'Yes', 1, 1),
('yes_no', 'N', 'No', 2, 1);

-- Weekdays
INSERT INTO dropdown_options (dropdown_name, value, label, order_index, is_active) VALUES
('weekdays', 'MON', 'Monday', 1, 1),
('weekdays', 'TUE', 'Tuesday', 2, 1),
('weekdays', 'WED', 'Wednesday', 3, 1),
('weekdays', 'THU', 'Thursday', 4, 1),
('weekdays', 'FRI', 'Friday', 5, 1),
('weekdays', 'SAT', 'Saturday', 6, 1),
('weekdays', 'SUN', 'Sunday', 7, 1);