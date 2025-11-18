"""
Script para importar as 185 agendas do arquivo import_agendas.sql no Supabase
"""
import os
import sys
from datetime import datetime
from supabase import create_client, Client

# Ler credenciais do arquivo secrets.toml
import toml

secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)

SUPABASE_URL = secrets["SUPABASE_URL"]
SUPABASE_KEY = secrets["SUPABASE_KEY"]

print(f"🔑 URL: {SUPABASE_URL}")
print(f"🔑 Key (primeiros 20 chars): {SUPABASE_KEY[:20]}...\n")

# Criar cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Dados das 185 agendas
agendas = [
    # André - 46 agendas
    {"consultor": "André", "projeto": "Projeto Alpha", "os": "1001", "data_inicio": "2025-02-10", "data_fim": "2025-02-20"},
    {"consultor": "André", "projeto": "Projeto Beta", "os": "1002", "data_inicio": "2025-02-25", "data_fim": "2025-03-05"},
    {"consultor": "André", "projeto": "Projeto Gamma", "os": "1003", "data_inicio": "2025-03-10", "data_fim": "2025-03-18"},
    {"consultor": "André", "projeto": "Projeto Delta", "os": "1004", "data_inicio": "2025-03-22", "data_fim": "2025-04-02"},
    {"consultor": "André", "projeto": "Projeto Epsilon", "os": "1005", "data_inicio": "2025-04-07", "data_fim": "2025-04-15"},
    {"consultor": "André", "projeto": "Projeto Zeta", "os": "1006", "data_inicio": "2025-04-20", "data_fim": "2025-04-28"},
    {"consultor": "André", "projeto": "Projeto Eta", "os": "1007", "data_inicio": "2025-05-03", "data_fim": "2025-05-12"},
    {"consultor": "André", "projeto": "Projeto Theta", "os": "1008", "data_inicio": "2025-05-17", "data_fim": "2025-05-25"},
    {"consultor": "André", "projeto": "Projeto Iota", "os": "1009", "data_inicio": "2025-05-30", "data_fim": "2025-06-08"},
    {"consultor": "André", "projeto": "Projeto Kappa", "os": "1010", "data_inicio": "2025-06-13", "data_fim": "2025-06-22"},
    {"consultor": "André", "projeto": "Projeto Lambda", "os": "1011", "data_inicio": "2025-06-27", "data_fim": "2025-07-06"},
    {"consultor": "André", "projeto": "Projeto Mu", "os": "1012", "data_inicio": "2025-07-11", "data_fim": "2025-07-20"},
    {"consultor": "André", "projeto": "Projeto Nu", "os": "1013", "data_inicio": "2025-07-25", "data_fim": "2025-08-03"},
    {"consultor": "André", "projeto": "Projeto Xi", "os": "1014", "data_inicio": "2025-08-08", "data_fim": "2025-08-17"},
    {"consultor": "André", "projeto": "Projeto Omicron", "os": "1015", "data_inicio": "2025-08-22", "data_fim": "2025-08-31"},
    {"consultor": "André", "projeto": "Projeto Pi", "os": "1016", "data_inicio": "2025-09-05", "data_fim": "2025-09-14"},
    {"consultor": "André", "projeto": "Projeto Rho", "os": "1017", "data_inicio": "2025-09-19", "data_fim": "2025-09-28"},
    {"consultor": "André", "projeto": "Projeto Sigma", "os": "1018", "data_inicio": "2025-10-03", "data_fim": "2025-10-12"},
    {"consultor": "André", "projeto": "Projeto Tau", "os": "1019", "data_inicio": "2025-10-17", "data_fim": "2025-10-26"},
    {"consultor": "André", "projeto": "Projeto Upsilon", "os": "1020", "data_inicio": "2025-10-31", "data_fim": "2025-11-09"},
    {"consultor": "André", "projeto": "Projeto Phi", "os": "1021", "data_inicio": "2025-11-14", "data_fim": "2025-11-23"},
    {"consultor": "André", "projeto": "Projeto Chi", "os": "1022", "data_inicio": "2025-11-28", "data_fim": "2025-12-07"},
    {"consultor": "André", "projeto": "Projeto Psi", "os": "1023", "data_inicio": "2025-12-12", "data_fim": "2025-12-21"},
    {"consultor": "André", "projeto": "Projeto Omega", "os": "1024", "data_inicio": "2025-12-26", "data_fim": "2026-01-04"},
    {"consultor": "André", "projeto": "Projeto Nova", "os": "1025", "data_inicio": "2026-01-09", "data_fim": "2026-01-18"},
    {"consultor": "André", "projeto": "Projeto Stellar", "os": "1026", "data_inicio": "2026-01-23", "data_fim": "2026-02-01"},
    {"consultor": "André", "projeto": "Projeto Nebula", "os": "1027", "data_inicio": "2025-02-12", "data_fim": "2025-02-16"},
    {"consultor": "André", "projeto": "Projeto Quantum", "os": "1028", "data_inicio": "2025-03-05", "data_fim": "2025-03-09"},
    {"consultor": "André", "projeto": "Projeto Fusion", "os": "1029", "data_inicio": "2025-04-01", "data_fim": "2025-04-05"},
    {"consultor": "André", "projeto": "Projeto Infinity", "os": "1030", "data_inicio": "2025-05-01", "data_fim": "2025-05-06"},
    {"consultor": "André", "projeto": "Projeto Matrix", "os": "1031", "data_inicio": "2025-06-02", "data_fim": "2025-06-07"},
    {"consultor": "André", "projeto": "Projeto Vector", "os": "1032", "data_inicio": "2025-07-03", "data_fim": "2025-07-08"},
    {"consultor": "André", "projeto": "Projeto Nexus", "os": "1033", "data_inicio": "2025-08-01", "data_fim": "2025-08-06"},
    {"consultor": "André", "projeto": "Projeto Prism", "os": "1034", "data_inicio": "2025-09-02", "data_fim": "2025-09-07"},
    {"consultor": "André", "projeto": "Projeto Pulse", "os": "1035", "data_inicio": "2025-10-01", "data_fim": "2025-10-06"},
    {"consultor": "André", "projeto": "Projeto Vortex", "os": "1036", "data_inicio": "2025-11-03", "data_fim": "2025-11-08"},
    {"consultor": "André", "projeto": "Projeto Zenith", "os": "1037", "data_inicio": "2025-12-01", "data_fim": "2025-12-06"},
    {"consultor": "André", "projeto": "Projeto Aurora", "os": "1038", "data_inicio": "2026-01-05", "data_fim": "2026-01-10"},
    {"consultor": "André", "projeto": "Projeto Cosmos", "os": "1039", "data_inicio": "2025-02-18", "data_fim": "2025-02-22"},
    {"consultor": "André", "projeto": "Projeto Eclipse", "os": "1040", "data_inicio": "2025-03-15", "data_fim": "2025-03-20"},
    {"consultor": "André", "projeto": "Projeto Horizon", "os": "1041", "data_inicio": "2025-04-12", "data_fim": "2025-04-17"},
    {"consultor": "André", "projeto": "Projeto Meteor", "os": "1042", "data_inicio": "2025-05-22", "data_fim": "2025-05-27"},
    {"consultor": "André", "projeto": "Projeto Orbit", "os": "1043", "data_inicio": "2025-06-18", "data_fim": "2025-06-23"},
    {"consultor": "André", "projeto": "Projeto Parallax", "os": "1044", "data_inicio": "2025-07-16", "data_fim": "2025-07-21"},
    {"consultor": "André", "projeto": "Projeto Quasar", "os": "1045", "data_inicio": "2025-08-13", "data_fim": "2025-08-18"},
    {"consultor": "André", "projeto": "Projeto Radiance", "os": "1046", "data_inicio": "2025-09-10", "data_fim": "2025-09-15"},
    
    # Gracina - 20 agendas
    {"consultor": "Gracina", "projeto": "Projeto Solar", "os": "2001", "data_inicio": "2025-02-05", "data_fim": "2025-02-12"},
    {"consultor": "Gracina", "projeto": "Projeto Lunar", "os": "2002", "data_inicio": "2025-02-15", "data_fim": "2025-02-22"},
    {"consultor": "Gracina", "projeto": "Projeto Mars", "os": "2003", "data_inicio": "2025-03-01", "data_fim": "2025-03-08"},
    {"consultor": "Gracina", "projeto": "Projeto Jupiter", "os": "2004", "data_inicio": "2025-03-15", "data_fim": "2025-03-22"},
    {"consultor": "Gracina", "projeto": "Projeto Saturn", "os": "2005", "data_inicio": "2025-04-01", "data_fim": "2025-04-08"},
    {"consultor": "Gracina", "projeto": "Projeto Neptune", "os": "2006", "data_inicio": "2025-04-15", "data_fim": "2025-04-22"},
    {"consultor": "Gracina", "projeto": "Projeto Venus", "os": "2007", "data_inicio": "2025-05-01", "data_fim": "2025-05-08"},
    {"consultor": "Gracina", "projeto": "Projeto Mercury", "os": "2008", "data_inicio": "2025-05-15", "data_fim": "2025-05-22"},
    {"consultor": "Gracina", "projeto": "Projeto Pluto", "os": "2009", "data_inicio": "2025-06-01", "data_fim": "2025-06-08"},
    {"consultor": "Gracina", "projeto": "Projeto Uranus", "os": "2010", "data_inicio": "2025-06-15", "data_fim": "2025-06-22"},
    {"consultor": "Gracina", "projeto": "Projeto Comet", "os": "2011", "data_inicio": "2025-07-01", "data_fim": "2025-07-08"},
    {"consultor": "Gracina", "projeto": "Projeto Asteroid", "os": "2012", "data_inicio": "2025-07-15", "data_fim": "2025-07-22"},
    {"consultor": "Gracina", "projeto": "Projeto Galaxy", "os": "2013", "data_inicio": "2025-02-08", "data_fim": "2025-02-11"},
    {"consultor": "Gracina", "projeto": "Projeto Supernova", "os": "2014", "data_inicio": "2025-03-10", "data_fim": "2025-03-13"},
    {"consultor": "Gracina", "projeto": "Projeto Blackhole", "os": "2015", "data_inicio": "2025-04-10", "data_fim": "2025-04-13"},
    {"consultor": "Gracina", "projeto": "Projeto Stardust", "os": "2016", "data_inicio": "2025-05-10", "data_fim": "2025-05-13"},
    {"consultor": "Gracina", "projeto": "Projeto Constellation", "os": "2017", "data_inicio": "2025-06-10", "data_fim": "2025-06-13"},
    {"consultor": "Gracina", "projeto": "Projeto Milkyway", "os": "2018", "data_inicio": "2025-07-10", "data_fim": "2025-07-13"},
    {"consultor": "Gracina", "projeto": "Projeto Andromeda", "os": "2019", "data_inicio": "2025-02-25", "data_fim": "2025-02-28"},
    {"consultor": "Gracina", "projeto": "Projeto Orion", "os": "2020", "data_inicio": "2025-03-25", "data_fim": "2025-03-28"},
    
    # Sirlene - 31 agendas
    {"consultor": "Sirlene", "projeto": "Projeto Atlantis", "os": "3001", "data_inicio": "2025-03-01", "data_fim": "2025-03-10"},
    {"consultor": "Sirlene", "projeto": "Projeto Olympus", "os": "3002", "data_inicio": "2025-03-15", "data_fim": "2025-03-24"},
    {"consultor": "Sirlene", "projeto": "Projeto Phoenix", "os": "3003", "data_inicio": "2025-04-01", "data_fim": "2025-04-10"},
    {"consultor": "Sirlene", "projeto": "Projeto Dragon", "os": "3004", "data_inicio": "2025-04-15", "data_fim": "2025-04-24"},
    {"consultor": "Sirlene", "projeto": "Projeto Pegasus", "os": "3005", "data_inicio": "2025-05-01", "data_fim": "2025-05-10"},
    {"consultor": "Sirlene", "projeto": "Projeto Titan", "os": "3006", "data_inicio": "2025-05-15", "data_fim": "2025-05-24"},
    {"consultor": "Sirlene", "projeto": "Projeto Hercules", "os": "3007", "data_inicio": "2025-06-01", "data_fim": "2025-06-10"},
    {"consultor": "Sirlene", "projeto": "Projeto Apollo", "os": "3008", "data_inicio": "2025-06-15", "data_fim": "2025-06-24"},
    {"consultor": "Sirlene", "projeto": "Projeto Zeus", "os": "3009", "data_inicio": "2025-07-01", "data_fim": "2025-07-10"},
    {"consultor": "Sirlene", "projeto": "Projeto Athena", "os": "3010", "data_inicio": "2025-07-15", "data_fim": "2025-07-24"},
    {"consultor": "Sirlene", "projeto": "Projeto Poseidon", "os": "3011", "data_inicio": "2025-08-01", "data_fim": "2025-08-10"},
    {"consultor": "Sirlene", "projeto": "Projeto Hades", "os": "3012", "data_inicio": "2025-08-15", "data_fim": "2025-08-24"},
    {"consultor": "Sirlene", "projeto": "Projeto Artemis", "os": "3013", "data_inicio": "2025-09-01", "data_fim": "2025-09-10"},
    {"consultor": "Sirlene", "projeto": "Projeto Ares", "os": "3014", "data_inicio": "2025-09-15", "data_fim": "2025-09-24"},
    {"consultor": "Sirlene", "projeto": "Projeto Hera", "os": "3015", "data_inicio": "2025-10-01", "data_fim": "2025-10-10"},
    {"consultor": "Sirlene", "projeto": "Projeto Demeter", "os": "3016", "data_inicio": "2025-10-15", "data_fim": "2025-10-24"},
    {"consultor": "Sirlene", "projeto": "Projeto Hephaestus", "os": "3017", "data_inicio": "2025-11-01", "data_fim": "2025-11-10"},
    {"consultor": "Sirlene", "projeto": "Projeto Aphrodite", "os": "3018", "data_inicio": "2025-11-15", "data_fim": "2025-11-24"},
    {"consultor": "Sirlene", "projeto": "Projeto Hermes", "os": "3019", "data_inicio": "2025-12-01", "data_fim": "2025-12-10"},
    {"consultor": "Sirlene", "projeto": "Projeto Dionysus", "os": "3020", "data_inicio": "2025-12-15", "data_fim": "2025-12-24"},
    {"consultor": "Sirlene", "projeto": "Projeto Persephone", "os": "3021", "data_inicio": "2025-03-05", "data_fim": "2025-03-08"},
    {"consultor": "Sirlene", "projeto": "Projeto Helios", "os": "3022", "data_inicio": "2025-04-05", "data_fim": "2025-04-08"},
    {"consultor": "Sirlene", "projeto": "Projeto Selene", "os": "3023", "data_inicio": "2025-05-05", "data_fim": "2025-05-08"},
    {"consultor": "Sirlene", "projeto": "Projeto Eos", "os": "3024", "data_inicio": "2025-06-05", "data_fim": "2025-06-08"},
    {"consultor": "Sirlene", "projeto": "Projeto Nyx", "os": "3025", "data_inicio": "2025-07-05", "data_fim": "2025-07-08"},
    {"consultor": "Sirlene", "projeto": "Projeto Chaos", "os": "3026", "data_inicio": "2025-08-05", "data_fim": "2025-08-08"},
    {"consultor": "Sirlene", "projeto": "Projeto Gaia", "os": "3027", "data_inicio": "2025-09-05", "data_fim": "2025-09-08"},
    {"consultor": "Sirlene", "projeto": "Projeto Uranus", "os": "3028", "data_inicio": "2025-10-05", "data_fim": "2025-10-08"},
    {"consultor": "Sirlene", "projeto": "Projeto Cronus", "os": "3029", "data_inicio": "2025-11-05", "data_fim": "2025-11-08"},
    {"consultor": "Sirlene", "projeto": "Projeto Rhea", "os": "3030", "data_inicio": "2025-12-05", "data_fim": "2025-12-08"},
    {"consultor": "Sirlene", "projeto": "Projeto Prometheus", "os": "3031", "data_inicio": "2025-03-20", "data_fim": "2025-03-23"},
    
    # Mayara - 40 agendas
    {"consultor": "Mayara", "projeto": "Projeto Atlas", "os": "4001", "data_inicio": "2025-02-01", "data_fim": "2025-02-08"},
    {"consultor": "Mayara", "projeto": "Projeto Everest", "os": "4002", "data_inicio": "2025-02-12", "data_fim": "2025-02-19"},
    {"consultor": "Mayara", "projeto": "Projeto Kilimanjaro", "os": "4003", "data_inicio": "2025-02-23", "data_fim": "2025-03-02"},
    {"consultor": "Mayara", "projeto": "Projeto McKinley", "os": "4004", "data_inicio": "2025-03-06", "data_fim": "2025-03-13"},
    {"consultor": "Mayara", "projeto": "Projeto Fuji", "os": "4005", "data_inicio": "2025-03-17", "data_fim": "2025-03-24"},
    {"consultor": "Mayara", "projeto": "Projeto Matterhorn", "os": "4006", "data_inicio": "2025-03-28", "data_fim": "2025-04-04"},
    {"consultor": "Mayara", "projeto": "Projeto Andes", "os": "4007", "data_inicio": "2025-04-08", "data_fim": "2025-04-15"},
    {"consultor": "Mayara", "projeto": "Projeto Alps", "os": "4008", "data_inicio": "2025-04-19", "data_fim": "2025-04-26"},
    {"consultor": "Mayara", "projeto": "Projeto Rockies", "os": "4009", "data_inicio": "2025-04-30", "data_fim": "2025-05-07"},
    {"consultor": "Mayara", "projeto": "Projeto Himalayas", "os": "4010", "data_inicio": "2025-05-11", "data_fim": "2025-05-18"},
    {"consultor": "Mayara", "projeto": "Projeto Cascade", "os": "4011", "data_inicio": "2025-05-22", "data_fim": "2025-05-29"},
    {"consultor": "Mayara", "projeto": "Projeto Sierra", "os": "4012", "data_inicio": "2025-06-02", "data_fim": "2025-06-09"},
    {"consultor": "Mayara", "projeto": "Projeto Pyrenees", "os": "4013", "data_inicio": "2025-06-13", "data_fim": "2025-06-20"},
    {"consultor": "Mayara", "projeto": "Projeto Appalachian", "os": "4014", "data_inicio": "2025-06-24", "data_fim": "2025-07-01"},
    {"consultor": "Mayara", "projeto": "Projeto Carpathian", "os": "4015", "data_inicio": "2025-07-05", "data_fim": "2025-07-12"},
    {"consultor": "Mayara", "projeto": "Projeto Ural", "os": "4016", "data_inicio": "2025-07-16", "data_fim": "2025-07-23"},
    {"consultor": "Mayara", "projeto": "Projeto Caucasus", "os": "4017", "data_inicio": "2025-07-27", "data_fim": "2025-08-03"},
    {"consultor": "Mayara", "projeto": "Projeto Tian Shan", "os": "4018", "data_inicio": "2025-08-07", "data_fim": "2025-08-14"},
    {"consultor": "Mayara", "projeto": "Projeto Altai", "os": "4019", "data_inicio": "2025-08-18", "data_fim": "2025-08-25"},
    {"consultor": "Mayara", "projeto": "Projeto Hindu Kush", "os": "4020", "data_inicio": "2025-08-29", "data_fim": "2025-09-05"},
    {"consultor": "Mayara", "projeto": "Projeto Karakoram", "os": "4021", "data_inicio": "2025-09-09", "data_fim": "2025-09-16"},
    {"consultor": "Mayara", "projeto": "Projeto Pamir", "os": "4022", "data_inicio": "2025-09-20", "data_fim": "2025-09-27"},
    {"consultor": "Mayara", "projeto": "Projeto Kunlun", "os": "4023", "data_inicio": "2025-10-01", "data_fim": "2025-10-08"},
    {"consultor": "Mayara", "projeto": "Projeto Zagros", "os": "4024", "data_inicio": "2025-10-12", "data_fim": "2025-10-19"},
    {"consultor": "Mayara", "projeto": "Projeto Elburz", "os": "4025", "data_inicio": "2025-10-23", "data_fim": "2025-10-30"},
    {"consultor": "Mayara", "projeto": "Projeto Taurus", "os": "4026", "data_inicio": "2025-11-03", "data_fim": "2025-11-10"},
    {"consultor": "Mayara", "projeto": "Projeto Pontus", "os": "4027", "data_inicio": "2025-11-14", "data_fim": "2025-11-21"},
    {"consultor": "Mayara", "projeto": "Projeto Balkans", "os": "4028", "data_inicio": "2025-11-25", "data_fim": "2025-12-02"},
    {"consultor": "Mayara", "projeto": "Projeto Dinaric", "os": "4029", "data_inicio": "2025-12-06", "data_fim": "2025-12-13"},
    {"consultor": "Mayara", "projeto": "Projeto Rhodope", "os": "4030", "data_inicio": "2025-12-17", "data_fim": "2025-12-24"},
    {"consultor": "Mayara", "projeto": "Projeto Pindus", "os": "4031", "data_inicio": "2025-12-28", "data_fim": "2026-01-04"},
    {"consultor": "Mayara", "projeto": "Projeto Olympus", "os": "4032", "data_inicio": "2026-01-08", "data_fim": "2026-01-15"},
    {"consultor": "Mayara", "projeto": "Projeto Parnassus", "os": "4033", "data_inicio": "2026-01-19", "data_fim": "2026-01-26"},
    {"consultor": "Mayara", "projeto": "Projeto Helicon", "os": "4034", "data_inicio": "2025-02-04", "data_fim": "2025-02-06"},
    {"consultor": "Mayara", "projeto": "Projeto Parnitha", "os": "4035", "data_inicio": "2025-03-04", "data_fim": "2025-03-06"},
    {"consultor": "Mayara", "projeto": "Projeto Taygetus", "os": "4036", "data_inicio": "2025-04-03", "data_fim": "2025-04-05"},
    {"consultor": "Mayara", "projeto": "Projeto Ida", "os": "4037", "data_inicio": "2025-05-05", "data_fim": "2025-05-07"},
    {"consultor": "Mayara", "projeto": "Projeto Othrys", "os": "4038", "data_inicio": "2025-06-04", "data_fim": "2025-06-06"},
    {"consultor": "Mayara", "projeto": "Projeto Pelion", "os": "4039", "data_inicio": "2025-07-04", "data_fim": "2025-07-06"},
    {"consultor": "Mayara", "projeto": "Projeto Ossa", "os": "4040", "data_inicio": "2025-08-04", "data_fim": "2025-08-06"},
    
    # Miguel - 32 agendas
    {"consultor": "Miguel", "projeto": "Projeto Amazon", "os": "5001", "data_inicio": "2025-03-01", "data_fim": "2025-03-09"},
    {"consultor": "Miguel", "projeto": "Projeto Nile", "os": "5002", "data_inicio": "2025-03-13", "data_fim": "2025-03-21"},
    {"consultor": "Miguel", "projeto": "Projeto Yangtze", "os": "5003", "data_inicio": "2025-03-25", "data_fim": "2025-04-02"},
    {"consultor": "Miguel", "projeto": "Projeto Mississippi", "os": "5004", "data_inicio": "2025-04-06", "data_fim": "2025-04-14"},
    {"consultor": "Miguel", "projeto": "Projeto Danube", "os": "5005", "data_inicio": "2025-04-18", "data_fim": "2025-04-26"},
    {"consultor": "Miguel", "projeto": "Projeto Rhine", "os": "5006", "data_inicio": "2025-04-30", "data_fim": "2025-05-08"},
    {"consultor": "Miguel", "projeto": "Projeto Congo", "os": "5007", "data_inicio": "2025-05-12", "data_fim": "2025-05-20"},
    {"consultor": "Miguel", "projeto": "Projeto Ganges", "os": "5008", "data_inicio": "2025-05-24", "data_fim": "2025-06-01"},
    {"consultor": "Miguel", "projeto": "Projeto Mekong", "os": "5009", "data_inicio": "2025-06-05", "data_fim": "2025-06-13"},
    {"consultor": "Miguel", "projeto": "Projeto Thames", "os": "5010", "data_inicio": "2025-06-17", "data_fim": "2025-06-25"},
    {"consultor": "Miguel", "projeto": "Projeto Seine", "os": "5011", "data_inicio": "2025-06-29", "data_fim": "2025-07-07"},
    {"consultor": "Miguel", "projeto": "Projeto Tiber", "os": "5012", "data_inicio": "2025-07-11", "data_fim": "2025-07-19"},
    {"consultor": "Miguel", "projeto": "Projeto Volga", "os": "5013", "data_inicio": "2025-07-23", "data_fim": "2025-07-31"},
    {"consultor": "Miguel", "projeto": "Projeto Indus", "os": "5014", "data_inicio": "2025-08-04", "data_fim": "2025-08-12"},
    {"consultor": "Miguel", "projeto": "Projeto Euphrates", "os": "5015", "data_inicio": "2025-08-16", "data_fim": "2025-08-24"},
    {"consultor": "Miguel", "projeto": "Projeto Tigris", "os": "5016", "data_inicio": "2025-08-28", "data_fim": "2025-09-05"},
    {"consultor": "Miguel", "projeto": "Projeto Jordan", "os": "5017", "data_inicio": "2025-09-09", "data_fim": "2025-09-17"},
    {"consultor": "Miguel", "projeto": "Projeto Zambezi", "os": "5018", "data_inicio": "2025-09-21", "data_fim": "2025-09-29"},
    {"consultor": "Miguel", "projeto": "Projeto Niger", "os": "5019", "data_inicio": "2025-10-03", "data_fim": "2025-10-11"},
    {"consultor": "Miguel", "projeto": "Projeto Orange", "os": "5020", "data_inicio": "2025-10-15", "data_fim": "2025-10-23"},
    {"consultor": "Miguel", "projeto": "Projeto Limpopo", "os": "5021", "data_inicio": "2025-10-27", "data_fim": "2025-11-04"},
    {"consultor": "Miguel", "projeto": "Projeto Murray", "os": "5022", "data_inicio": "2025-11-08", "data_fim": "2025-11-16"},
    {"consultor": "Miguel", "projeto": "Projeto Darling", "os": "5023", "data_inicio": "2025-11-20", "data_fim": "2025-11-28"},
    {"consultor": "Miguel", "projeto": "Projeto Colorado", "os": "5024", "data_inicio": "2025-12-02", "data_fim": "2025-12-10"},
    {"consultor": "Miguel", "projeto": "Projeto Columbia", "os": "5025", "data_inicio": "2025-12-14", "data_fim": "2025-12-22"},
    {"consultor": "Miguel", "projeto": "Projeto Rio Grande", "os": "5026", "data_inicio": "2025-03-05", "data_fim": "2025-03-08"},
    {"consultor": "Miguel", "projeto": "Projeto Orinoco", "os": "5027", "data_inicio": "2025-04-04", "data_fim": "2025-04-07"},
    {"consultor": "Miguel", "projeto": "Projeto Parana", "os": "5028", "data_inicio": "2025-05-05", "data_fim": "2025-05-08"},
    {"consultor": "Miguel", "projeto": "Projeto São Francisco", "os": "5029", "data_inicio": "2025-06-03", "data_fim": "2025-06-06"},
    {"consultor": "Miguel", "projeto": "Projeto Uruguay", "os": "5030", "data_inicio": "2025-07-03", "data_fim": "2025-07-06"},
    {"consultor": "Miguel", "projeto": "Projeto Paraguay", "os": "5031", "data_inicio": "2025-08-02", "data_fim": "2025-08-05"},
    {"consultor": "Miguel", "projeto": "Projeto Magdalena", "os": "5032", "data_inicio": "2025-09-02", "data_fim": "2025-09-05"},
    
    # Lucas - 16 agendas
    {"consultor": "Lucas", "projeto": "Projeto Pacific", "os": "6001", "data_inicio": "2025-07-01", "data_fim": "2025-07-10"},
    {"consultor": "Lucas", "projeto": "Projeto Atlantic", "os": "6002", "data_inicio": "2025-07-15", "data_fim": "2025-07-24"},
    {"consultor": "Lucas", "projeto": "Projeto Indian", "os": "6003", "data_inicio": "2025-08-01", "data_fim": "2025-08-10"},
    {"consultor": "Lucas", "projeto": "Projeto Arctic", "os": "6004", "data_inicio": "2025-08-15", "data_fim": "2025-08-24"},
    {"consultor": "Lucas", "projeto": "Projeto Antarctic", "os": "6005", "data_inicio": "2025-09-01", "data_fim": "2025-09-10"},
    {"consultor": "Lucas", "projeto": "Projeto Mediterranean", "os": "6006", "data_inicio": "2025-09-15", "data_fim": "2025-09-24"},
    {"consultor": "Lucas", "projeto": "Projeto Caribbean", "os": "6007", "data_inicio": "2025-10-01", "data_fim": "2025-10-10"},
    {"consultor": "Lucas", "projeto": "Projeto Red Sea", "os": "6008", "data_inicio": "2025-10-15", "data_fim": "2025-10-24"},
    {"consultor": "Lucas", "projeto": "Projeto Black Sea", "os": "6009", "data_inicio": "2025-11-01", "data_fim": "2025-11-10"},
    {"consultor": "Lucas", "projeto": "Projeto Caspian", "os": "6010", "data_inicio": "2025-11-15", "data_fim": "2025-11-24"},
    {"consultor": "Lucas", "projeto": "Projeto Coral", "os": "6011", "data_inicio": "2025-07-05", "data_fim": "2025-07-08"},
    {"consultor": "Lucas", "projeto": "Projeto Aegean", "os": "6012", "data_inicio": "2025-08-05", "data_fim": "2025-08-08"},
    {"consultor": "Lucas", "projeto": "Projeto Adriatic", "os": "6013", "data_inicio": "2025-09-05", "data_fim": "2025-09-08"},
    {"consultor": "Lucas", "projeto": "Projeto Baltic", "os": "6014", "data_inicio": "2025-10-05", "data_fim": "2025-10-08"},
    {"consultor": "Lucas", "projeto": "Projeto North Sea", "os": "6015", "data_inicio": "2025-11-05", "data_fim": "2025-11-08"},
    {"consultor": "Lucas", "projeto": "Projeto Persian Gulf", "os": "6016", "data_inicio": "2025-07-20", "data_fim": "2025-07-23"},
]

def importar_agendas():
    """Importa todas as agendas no Supabase"""
    print(f"🚀 Iniciando importação de {len(agendas)} agendas...\n")
    
    sucesso = 0
    erros = 0
    
    for i, agenda in enumerate(agendas, 1):
        try:
            result = supabase.table("agendas").insert(agenda).execute()
            sucesso += 1
            print(f"✅ [{i}/{len(agendas)}] Importado: {agenda['consultor']} - {agenda['projeto']}")
        except Exception as e:
            erros += 1
            print(f"❌ [{i}/{len(agendas)}] Erro ao importar {agenda['consultor']} - {agenda['projeto']}: {str(e)}")
    
    print(f"\n📊 Importação concluída!")
    print(f"   ✅ Sucesso: {sucesso}")
    print(f"   ❌ Erros: {erros}")
    print(f"   📈 Total: {len(agendas)}")

if __name__ == "__main__":
    importar_agendas()
