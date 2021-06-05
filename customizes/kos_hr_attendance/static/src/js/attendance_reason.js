odoo.define("kos_hr_attendance.attendances_reason", function(require) {
    "use strict";
    var checkin_status = "";
    var checkout_status = "";
    var MyAttendances = require("hr_attendance.my_attendances");
    var field_utils = require('web.field_utils');
    // Star Working Time is 08:30:00 - format new Date(Y,M,D,H,M,S);
    var startDateTime = new Date(2020,12,12,8,30,0);
    // Get Time
    var startWorkingTime = startDateTime.toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit', second:'2-digit', hour12 : false});
    function test_hour_after_9am(base_hour, base_minutes, base_second){
        let current_date = new Date();
        let base_condition = new Date();
        base_condition.setHours(base_hour);
        base_condition.setMinutes(base_minutes);
        base_condition.setSeconds(base_second);
        let diffInMinutes = (current_date.getTime() - base_condition.getTime()) / 60000;
        let diffInHours = diffInMinutes / 60;
        return diffInHours;
    }

    MyAttendances.include({
        events: {
            "click .o_hr_attendance_sign_in_out_icon": _.debounce(function(event) {
//                alert(event.target.attributes.title.value);
                  var click_action = event.target.attributes['click_action'].value;
                  var title = event.target.attributes.title.value;
                  if(click_action == "Sign in")
                  {
                    checkin_status = title;
                  }
                  else
                  {
                    checkout_status = title;
                  }
                this.update_attendance();
            }, 200, true),
        },
        willStart: function () {
        	var self = this;
            var def = this._rpc({
                    model: 'hr.employee',
                    method: 'search_read',
                    args: [[['user_id', '=', this.getSession().uid]], ['attendance_state', 'name', 'hours_today']],
                })
                .then(function (res) {
                    self.employee = res.length && res[0];
                    if (res.length) {
                        self.hours_today = field_utils.format.float_time(self.employee.hours_today);
                        self.late_working = new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit', second:'2-digit', hour12 : false}) > startWorkingTime;
                    }
                });

            return Promise.all([def, this._super.apply(this, arguments)]);
        },
        
        update_attendance: function () {
            var self = this;
            let reason = typeof($('.o_hr_attendance_REASONbox').val()) == 'undefined' ? null : $('.o_hr_attendance_REASONbox').val().trim();

            if(reason === '' && test_hour_after_9am(9,0,0) > 0)
        	{
            	self.do_warn('Please enter Reason for late working before click to Check-in!');
        	}
            else
            {
	            self._rpc({
	                    model: 'hr.employee',
	                    method: 'attendance_manual',
	                    args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances',
	                    	null,
	                    	self.$('.o_hr_attendance_REASONbox').val(),
	                    	checkin_status,
	                    	checkout_status
	                    	],
	                })
	                .then(function(result) {
	                    if (result.action) {
	                        self.do_action(result.action);
	                    } else if (result.warning) {
	                        self.do_warn(result.warning);
	                    }
	                });
            }
        },
    });
});