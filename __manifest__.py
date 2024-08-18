# -*- coding: utf-8 -*-


{
    'name': 'hospital',
    'version': '1.0.0',
    'category': 'hospital',
    'summary': 'hospital manegment system',
    'description': """hospital system""",
    'author': 'Dev abdulrhman',
    'depends': ['mail','product','report_xlsx','sale','stock','base'],
    'data': [
    "security/ir.model.access.csv",
    "data/patient_tag_data.xml",
    "data/sequnce_view.xml",
    "data/sequnce_appointment_view.xml",
    "data/patient.tag.csv",
    "wizard/cancel_appointment_veiw.xml",
    "wizard/search_appointment_view.xml",
    "veiws/menu.xml",
    "veiws/patient_veiw.xml",
    "veiws/appointment_veiw.xml",
    "veiws/female_patient_veiw.xml",
    "veiws/male_patient_view.xml",
    "veiws/patient_tag_view.xml",
    "veiws/odoo_play_ground.xml",
    "veiws/res_config_settings_views.xml",
    "veiws/operation_veiw.xml",
    "report/report.xml",
    "report/patient_card.xml",
    "report/patient_details_template.xml",




    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
     'License': 'LGPL-3',
    'application': True,
    'sequence': -100,

}
