"""Company content for the homepage and service pages.

Sources: the owner's live website (services, project-scope, clients, about and team pages)
and owner-supplied project scopes. See docs/CONTENT-SOURCES.md.
"""

CLIENTS = [
    {'name': 'PT PELNI (Persero)', 'logo': 'client-pelni.webp', 'width': 526, 'height': 160},
    {'name': 'Pertamina', 'logo': 'client-pertamina.svg', 'width': 1097, 'height': 255},
    {'name': 'Pelindo', 'logo': 'client-pelindo.webp', 'width': 774, 'height': 160},
    {'name': 'TNI Angkatan Laut (Indonesian Navy)', 'logo': 'client-tni-al.webp', 'width': 141, 'height': 160, 'emblem': True},
    {'name': 'PT Samudera Indonesia Tbk', 'logo': 'client-samudera-indonesia.webp', 'width': 1040, 'height': 160},
    {'name': 'PT USDA Seroja Jaya shipyard', 'logo': 'client-usda-seroja-jaya.webp', 'width': 588, 'height': 144},
    {'name': 'PT Armada Cakrawala Esa', 'logo': 'client-armada-cakrawala-esa.webp', 'width': 179, 'height': 53},
]

# Names and roles from the owner's reference; portraits from the original site.
LEADERSHIP = [
    {'name': 'Arif Fatkur Rohman, S.T., M.MT.', 'role': 'Director', 'image': 'leadership-arif', 'height': 870},
    {'name': 'M Rosul Akbar', 'role': 'Manager', 'image': 'leadership-rosul', 'height': 708},
    {'name': 'Anjas Budiarso', 'role': 'Manager', 'image': 'leadership-anjas', 'height': 960},
]

# Work gallery paused at the owner's request; keep these photos for later reuse.
# Owner-provided photos, 14 October 2026. Captions describe the visible work;
# project/vessel names and exact job scope have not been supplied.
WORK_PHOTOS = [
    {'stem': 'work-engine-room', 'width': 1280, 'height': 596,
     'title': 'Marine machinery', 'caption': 'Engineering work in the engine room.',
     'alt': 'Araya personnel working around machinery in a vessel’s engine room'},
    {'stem': 'work-switchboard', 'width': 1280, 'height': 960,
     'title': 'Electrical systems', 'caption': 'Onboard switchboard inspection and technical review.',
     'alt': 'Araya personnel reviewing an onboard electrical switchboard'},
]

# label, service page, anchor on that page
CAPABILITIES = [
    ('Fire alarm & monitoring', 'marine', 'alarms'),
    ('Engine safety devices', 'marine', 'safety'),
    ('Generator systems', 'marine', 'generators'),
    ('Manoeuvring, CPP & bow thrusters', 'marine', 'propulsion'),
    ('Deck cranes', 'marine', 'cranes'),
    ('CNC & wire-cut machines', 'industrial', 'machinery'),
    ('Industrial cranes', 'industrial', 'cranes'),
    ('MV/LV generators', 'industrial', 'generators'),
    ('PLC, HMI & SCADA', 'automation', 'plc'),
    ('Switchboards & MCC', 'automation', 'panels'),
    ('Hazardous-area equipment', 'automation', 'hazardous'),
    ('Electronic card repair', 'automation', 'electronics'),
]

BRAND_GROUPS = [
    ('Automation & control', ['Siemens', 'ABB', 'Schneider Electric', 'Omron', 'Mitsubishi', 'Allen-Bradley', 'Honeywell', 'Modicon']),
    ('Marine systems', ['Consilium', 'Autronica', 'Tyco', 'MEDC', 'SIMOS', 'MaK', 'Janssen', 'Stein Sohn']),
    ('Power generation', ['Stamford', 'Leroy-Somer', 'Marathon', 'Caterpillar', 'SDMO', 'Denyo', 'GE']),
    ('Hazardous area', ['Stahl', 'Chalmit', 'Crouse-Hinds', 'CEAG', 'Glamox', 'Orga']),
    ('Machine tools', ['Fanuc', 'Okuma', 'Makino', 'Mori Seiki', 'Toshiba', 'Charmilles']),
]

SERVICES = {
    'marine': {
        'name': 'Marine', 'short': 'marine', 'label': 'Marine engineering',
        'title': 'Marine Electrical & Automation Services Indonesia | Araya',
        'description': 'Ship maintenance, repair and retrofit across Indonesia, with offices in Surabaya and Jakarta. Electrical, mechanical and automation systems for ships.',
        'heading': 'Marine engineering.<br>Engine room to bridge.',
        'intro': 'Ship maintenance, repair and retrofit services across Indonesia, with offices in Surabaya and Jakarta.',
        'hero_image': 'marine-date-free.webp', 'hero_width': 767, 'hero_height': 883, 'hero_alt': 'Araya technician inspecting marine engine equipment',
        'card_image': 'marine-date-free.webp', 'card_width': 767, 'card_height': 883, 'card_alt': 'Technical inspection of marine engine equipment',
        'summary': 'Supply and repair of onboard systems, from engine room to bridge.',
        'highlights': ['Fire alarm, general alarm & monitoring', 'Engine safety devices', 'Manoeuvring, CPP & bow thrusters', 'Deck cranes, AC & refrigeration'],
        'scope_heading': 'Systems we repair,<br>upgrade and retrofit.',
        'overview': 'We supply and repair onboard systems, and modify, upgrade or retrofit obsolete and end-of-sale equipment so it can stay in service.',
        'groups': [
            ('alarms', 'Fire alarm, general alarm & AMS', 'Installation, supply, repair and retrofit of ship fire alarms, general alarms and monitoring systems.'),
            ('safety', 'Engine safety devices', 'Supply and repair of safety, alarm and shutdown systems for main and auxiliary engines.'),
            ('engines', 'Engine overhaul, control & monitoring', 'Engine overhaul, repair, control and monitoring for marine propulsion and auxiliary systems.'),
            ('generators', 'Generator control & synchronisation', 'Supply and repair of marine generators, including automatic start/stop, synchronisation and load sharing.'),
            ('propulsion', 'Steering, manoeuvring, CPP & bow thrusters', 'Repair and retrofit of steering, manoeuvring, controllable-pitch propeller and bow-thruster control systems.'),
            ('navigation', 'Navigation & public address', 'Service and repair of marine navigation and public-address equipment.'),
            ('automation', 'Electrical panels, PLC & SCADA', 'Repair and retrofit of marine electrical installations, control panels, PLC, HMI and SCADA systems.'),
            ('water-level', 'Water-level monitoring', 'Supply, replacement and integration of water-level monitoring systems for tanks and bilges.'),
            ('cargo-monitoring', 'Cargo monitoring systems', 'Supply, repair and retrofit of cargo monitoring systems and related sensors.'),
            ('cranes', 'Deck cranes & deck machinery', 'Supply and repair of deck cranes, deck machinery and their control systems.'),
            ('hvac', 'AC & refrigeration systems', 'Supply and repair of marine air-conditioning and refrigeration systems.'),
            ('retrofit', 'Retrofit of obsolete systems', 'Modification, upgrade and retrofit of obsolete marine equipment and control systems.'),
        ],
        'equipment': [
            ('Fire & alarm systems', ['Consilium', 'Autronica', 'Siemens', 'Tyco', 'Honeywell', 'MEDC', 'Hekatron']),
            ('Manoeuvring & propulsion', ['SIMOS', 'CAMOS', 'Stein Sohn', 'MaK', 'Janssen']),
            ('Monitoring & engine control', ['Noris', 'ComAp', 'Sinpol-D']),
            ('Generators', ['Stamford', 'Leroy-Somer', 'ABB', 'Marathon', 'GE']),
        ],
        'featured': [('noris', 'Speed, temperature and pressure sensors, indicators, noriMos AMS, noriStar propulsion control and noriNet remote monitoring.'),
                     ('comap', 'Marine engine controllers, generator synchronisation, load sharing and vessel power management.')],
        'enquiry': ['Vessel name, type and current location', 'Equipment make, model and nameplate photo', 'Fault symptoms, alarm messages or the change you need', 'Wiring diagrams or system drawings, if available', 'Planned docking or maintenance window'],
    },
    'industrial': {
        'name': 'Industrial', 'short': 'industrial', 'label': 'Industrial engineering',
        'title': 'Industrial Machinery, Crane & Generator Services | Araya',
        'description': 'Supply and repair of CNC, wire-cut and EDM machines, overhead and portal cranes, MV/LV generators and production machinery across Indonesia.',
        'heading': 'Industrial machinery.<br>Back in production.',
        'intro': 'Supply and repair of industrial machines, cranes and MV/LV generators.',
        'hero_image': 'industrial-date-free.webp', 'hero_width': 767, 'hero_height': 883, 'hero_alt': 'Araya engineer working inside an industrial electrical cabinet',
        'card_image': 'industrial-date-free.webp', 'card_width': 767, 'card_height': 883, 'card_alt': 'Industrial electrical installation from Araya’s service photography',
        'summary': 'Supply and repair of production machinery, cranes and power equipment.',
        'highlights': ['CNC, wire-cut & EDM machines', 'Overhead, portal & luffing cranes', 'MV/LV generators', 'Casting, moulding & cutting machines'],
        'scope_heading': 'Machines and equipment<br>we supply and repair.',
        'overview': 'We supply and repair industrial machines and cranes, together with the electrical and control equipment that runs them.',
        'groups': [
            ('machinery', 'CNC lathes & milling machines', 'Supply and repair of CNC lathes and milling machines.'),
            ('wirecut', 'Wire-cut & EDM machines', 'Supply and repair of wire-cut and electrical discharge machining (EDM) equipment.'),
            ('cutting', 'NC gas & plasma cutting', 'Service and repair of NC gas-cutting and plasma-cutting machines.'),
            ('production', 'Hobbing, casting & moulding', 'Supply and repair of hobbing, continuous-casting and moulding machines.'),
            ('cranes', 'Crane supply & repair', 'Supply and repair of industrial, overhead, portal and port cranes.'),
            ('generators', 'MV/LV generators', 'Supply and repair of medium- and low-voltage industrial generators.'),
            ('electrical', 'Panels & motor controls', 'Repair and modification of industrial electrical panels, switchboards and motor-control systems.'),
            ('automation', 'PLC, HMI & instrumentation', 'Programming, repair and integration of PLC, HMI and instrumentation systems for industrial automation.'),
        ],
        'equipment': [
            ('CNC & machine tools', ['Fanuc', 'Mitsubishi', 'Toshiba', 'Mori Seiki', 'Okuma', 'Makino']),
            ('Wire-cut & EDM', ['Charmilles', 'Fuji Electric', 'Fanuc']),
            ('Casting & cranes', ['CEIA', 'P&H']),
            ('Generators', ['GE', 'Leroy-Somer', 'Stamford', 'ABB', 'Marathon']),
        ],
        'featured': [('comap', 'Standby, prime-power and parallel generator control, load sharing and remote monitoring for industrial sites.'),
                     ('noris', 'Speed, temperature and pressure measurement, indicators and signal processing for machinery.')],
        'enquiry': ['Site name and location', 'Machine or generator make, model and nameplate photo', 'Fault symptoms, error codes or the upgrade you need', 'Electrical drawings and PLC/HMI project files, if available', 'Required completion date or shutdown window'],
    },
    'automation': {
        'name': 'Automation & Electrical', 'short': 'automation', 'label': 'Automation & electrical',
        'title': 'PLC, SCADA & Electrical Panel Services Indonesia | Araya',
        'description': 'PLC and SCADA software, switchboards and MCC, VFDs, hazardous-area equipment, protection relays and electronic card repair across Indonesia.',
        'heading': 'Automation &amp; electrical.<br>Control you can rely on.',
        'intro': 'PLC and SCADA, electrical power equipment, process instrumentation and electronic card repair.',
        'hero_image': 'control-room-1400.webp', 'hero_width': 1400, 'hero_height': 784, 'hero_variants': (('control-room-800.webp', 800), ('control-room-1400.webp', 1400)),
        'hero_alt': 'Marine control console with alarm panels and a Noris monitoring display',
        'card_image': 'work-control-room-diagnostics-900.webp', 'card_width': 900, 'card_height': 675,
        'card_variants': (('work-control-room-diagnostics-520.webp', 520), ('work-control-room-diagnostics-900.webp', 900)),
        'card_alt': 'Araya technician using a laptop at a ship control console',
        'summary': 'Control, power distribution and instrumentation for plants and vessels.',
        'highlights': ['PLC, HMI & SCADA', 'Switchboards, MCC & drives', 'Hazardous-area equipment', 'Protection relays & electronic cards'],
        'scope_heading': 'Control, power<br>and instrumentation.',
        'overview': 'We supply and repair the control, electrical power and instrumentation equipment that plants and vessels depend on.',
        'groups': [
            ('plc', 'PLC programming & retrofit', 'Supply, programming, repair and retrofit of PLC systems for marine and industrial automation.'),
            ('scada', 'SCADA & HMI software', 'SCADA and HMI software for system monitoring, alarms and operator control.'),
            ('instrumentation', 'Process control & instrumentation', 'Supply and integration of process-control systems, sensors and instrumentation.'),
            ('panels', 'Panels, switchboards & MCC', 'Supply, repair and modification of electrical panels, switchboards and motor-control centres.'),
            ('drives', 'Soft starters & VFDs', 'Supply and service of soft starters and variable-frequency drives for motor control.'),
            ('motors', 'Electric motors', 'Supply and service of industrial and hazardous-area electric motors.'),
            ('hazardous', 'Hazardous-area apparatus', 'Supply and repair of electrical equipment for hazardous-area installations.'),
            ('protection', 'Electrical protection', 'Supply and service of circuit breakers, fuses and electrical protection relays.'),
            ('power', 'Transformers, UPS & chargers', 'Supply and service of transformers, UPS systems and battery chargers.'),
            ('earthing', 'Surge protection, earthing & PFC', 'Supply and service of surge protection, earthing and power-factor correction equipment.'),
            ('gensets', 'Generators & generating sets', 'Supply, repair and control integration for generators and generating sets.'),
            ('electronics', 'Electronic card repair', 'Repair of electronic control boards for automation, machinery and electrical systems.'),
        ],
        'equipment': [
            ('PLC & control', ['Siemens', 'ABB', 'Omron', 'Mitsubishi', 'Allen-Bradley', 'Modicon', 'Honeywell']),
            ('Switchgear & MCC', ['Schneider Electric', 'Siemens', 'GE', 'Areva']),
            ('Drives & soft starters', ['Schneider Electric', 'Rockwell Automation', 'Allen-Bradley', 'ABB']),
            ('Protection relays', ['Sepam 2000', 'Sepam 1000+', 'Areva MiCOM']),
            ('Hazardous area', ['Stahl', 'Chalmit', 'Crouse-Hinds', 'CEAG', 'Glamox', 'Orga']),
            ('Motors', ['Siemens', 'ABB', 'Reliance']),
            ('Transformers, UPS & chargers', ['Unindo', 'Trafindo', 'Saft', 'Gutor', 'GE', 'ICA']),
            ('Generating sets', ['SDMO', 'Denyo', 'Caterpillar', 'Stamford', 'Leroy-Somer']),
            ('Cables & surge protection', ['Jembo', 'Kabelmetal', 'Pirelli', 'Supreme', 'Critec', 'Erico']),
        ],
        'featured': [('comap', 'Engine and generator controllers, power management, InteliSCADA and WebSupervisor monitoring.'),
                     ('noris', 'Sensors, signal processing, limit monitoring and integrated alarm and monitoring systems.')],
        'enquiry': ['Site or vessel and its location', 'Single-line diagram, panel drawings or I/O list', 'PLC/HMI platform and existing program backup, if available', 'Fault description, alarm history or the new functions required', 'Hazardous-area classification, where relevant'],
    },
}
