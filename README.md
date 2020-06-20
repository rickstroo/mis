# mis
Mass Immunization System

This project will create a mass immunization system (the "MIS").  MIS will use a FHIR server to store the immunization records, encounters and patients.  It is likely that this project will be launched as a SIIM 2020 Hack-A-Thon project.  The goal is to eventually deliver a solution to a health care provider.  It is likely that the solution will reside completely in the cloud.

For the SIIM 2020 Hack-A-Thon, we have created 3 teams.  These teams will work on one of 4 projects.  The source code for each project will be stored in a separate folder in the root folder of this repository.  Here are the names of the folders and the projects that they are related to.

patreg - Used for the Remote Registration project.  Will create a patient record and submit it to the FHIR server.
immrec - Used for the Immunization Resource project.  Will search for a patient, create an immunization record, and submit it to the FHIR server.
ehrint - Used for the EHR Integration project.  Will search for a patient, and their immunization records, and export one or more immunization records to an external EHR using HL7.
arrenc - Used for the Arrivals/Encounter project.  Will search for a patient, create an encounter record, and submit it to the FHIR server.
