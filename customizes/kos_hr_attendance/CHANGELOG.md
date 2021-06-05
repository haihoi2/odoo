# Changelog

All notable changes to this module will be documented in this file.

## [0.1] - 2020-12-15

### Added

- Default home is Check-in/Check-out page after login successfully
- Staff only see him-self/her-self attendances
- Manager can see all attendances

## [0.2] - 2020-12-28

### Added

- Add new field "Code" on Employee

### Changed

- About login by Google Email account

## [0.3] - 2020-12-29

### Added

- Go to Attandance list after checked-in or checked-out
- Constraint unique Employee code on a Company
- Hide some unnessessary menu (Home, Contact us...) on Website
- Add new button "Check-out" next to "Sign up" on Home page, this will be shown when attendance's status checked-in and logged-in
- Add new group Manager who can see their and their's staff attendances
- Text message "Welcome" replaced to "Welcome! Have a productive working day!" on Check-in form
- Move button "login with Google" over Email and Pass and note with Text
- Hide some unnessary tab informations (Work information, Private information, HR Settings)
  on Employee's form at first version - Only HR Manager see these tab now

### Changed

- Add Required attrs for field "Code"

## [0.4] - 2020-12-30

### Added

- Add field Code on Employee public
- Hide button Edit and Create on Attendance by access rights (Only Admin Attendance can edit)

## [0.5] - 2020-12-31

### Added

- Add new field "Checked-out IP" on Attendance

### Changed

- Label on Login's form: "For every members" to "For all members", "Only for Administrator" to "Only for Administrators"
- Label on Checked-out's form: Today's work hour to "Total time from last check-in"
- Label IP Address to "Checked-in IP" on Attendance

## [0.6] - 2020-12-31

### Added

- Function about Enter reason content on Checked-in Form after check-in at time over start working time (8h30)

## [0.7] - 2021-01-19

### Added

- Function check time before check-in in  
  \kos_hr_attendance\static\src\js\attendance_reason.js

## [0.8] - 2021-01-20

### Added

- SCSS file to style home element that help users easy to see in mobile screen
  kos_hr_attendance\static\scss\style.scss

### Changed

- Declare scss file into web.asset_backend by using template tag
  kos_hr_attendance\views\assets
  - fixed maxlength of o_hr_attendance_REASONbox text-center to 1000 characters (static/src/xml/attendance.xml)

## [0.9] - 2021-01-22

-Alter checkin button by status button icon:

How are you today?
Excellent  
Average
Poor

-Alter checkin button by status button icon:

How was your working day?
Excellent  
Average
Poor

-Added two columns "Checkin Status" and "Checkout Status" for manager. Has 3 values:
Excellent
Average
Poor

### Added
-Function check user id for prevent user create record for another and prevent user to pick a future day in check_in and check_out field

## [0.10] - 2021-02-05

Changed: Hide some feature that haven't launched

## [0.11] - 2021-02-18

Added: filter by manager name in attendance model

## [0.12] - 2021-03-31

Added new field to project model - field current_user: current user login -> feature Project manager can see all but fix own projects
Updated field Note from engineer : can be empty, not required
