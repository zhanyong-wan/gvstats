#!/usr/bin/env python3

import dataclasses
import enum


# A US state's political color.
class PoliticalColor(enum.Enum):
    BLUE = 0,  # Favors Democrats.
    LIGHT_BLUE = 1,
    PURPLE = 2,  # Neutral.
    LIGHT_RED = 3,
    RED = 4  # Favors Republicans.

    def __str__(self) -> str:
        # Turn "<PoliticalCOlor.RED: 4>" into RED.
        return self.__repr__().split(".")[1].split(":")[0]


# Maps a US state to its political color, based on the statewide result of
# 2008, 2012, 2016, and 2020 presidential elections.
#   BLUE: 4 wins for Democrats
#   LIGHT_BLUE: 3 wins for Democrats
#   PURPLE: 2 wins for each party
#   LIGHT_RED: 3 wins for Republicans
#   RED: 4 wins for Republicans
# Raw data: https://en.wikipedia.org/wiki/Red_states_and_blue_states
_STATE_CODE_TO_COLOR = {
    "WA": PoliticalColor.BLUE,
    "OR": PoliticalColor.BLUE,
    "CA": PoliticalColor.BLUE,
    "NV": PoliticalColor.BLUE,
    "CO": PoliticalColor.BLUE,
    "NM": PoliticalColor.BLUE,
    "HI": PoliticalColor.BLUE,
    "MN": PoliticalColor.BLUE,
    "IL": PoliticalColor.BLUE,
    "VA": PoliticalColor.BLUE,
    "MD": PoliticalColor.BLUE,
    "DE": PoliticalColor.BLUE,
    "NJ": PoliticalColor.BLUE,
    "CT": PoliticalColor.BLUE,
    "RI": PoliticalColor.BLUE,
    "MA": PoliticalColor.BLUE,
    "NH": PoliticalColor.BLUE,
    "ME": PoliticalColor.BLUE,
    "VT": PoliticalColor.BLUE,
    "NY": PoliticalColor.BLUE,

    "WI": PoliticalColor.LIGHT_BLUE,
    "MI": PoliticalColor.LIGHT_BLUE,
    "PA": PoliticalColor.LIGHT_BLUE,

    "IA": PoliticalColor.PURPLE,
    "OH": PoliticalColor.PURPLE,
    "FL": PoliticalColor.PURPLE,

    "IN": PoliticalColor.LIGHT_RED,
    "AZ": PoliticalColor.LIGHT_RED,
    "GA": PoliticalColor.LIGHT_RED,
    "NC": PoliticalColor.LIGHT_RED,

    "AK": PoliticalColor.RED,
    "MT": PoliticalColor.RED,
    "ID": PoliticalColor.RED,
    "UT": PoliticalColor.RED,
    "WY": PoliticalColor.RED,
    "ND": PoliticalColor.RED,
    "SD": PoliticalColor.RED,
    "NE": PoliticalColor.RED,
    "KS": PoliticalColor.RED,
    "OK": PoliticalColor.RED,
    "TX": PoliticalColor.RED,
    "MO": PoliticalColor.RED,
    "AR": PoliticalColor.RED,
    "LA": PoliticalColor.RED,
    "MS": PoliticalColor.RED,
    "AL": PoliticalColor.RED,
    "TN": PoliticalColor.RED,
    "KY": PoliticalColor.RED,
    "WV": PoliticalColor.RED,
    "SC": PoliticalColor.RED,
}

# Raw data: https://worldpopulationreview.com/states/state-abbreviations
_RAW_STATE_ABBREVIATIONS = [
    # ("state","abbrev","code"),
    ("Alabama","Ala.","AL"),
    ("Alaska","Alaska","AK"),
    ("Arizona","Ariz.","AZ"),
    ("Arkansas","Ark.","AR"),
    ("California","Calif.","CA"),
    ("Colorado","Colo.","CO"),
    ("Connecticut","Conn.","CT"),
    ("Delaware","Del.","DE"),
    ("District of Columbia","D.C.","DC"),
    ("Florida","Fla.","FL"),
    ("Georgia","Ga.","GA"),
    ("Hawaii","Hawaii","HI"),
    ("Idaho","Idaho","ID"),
    ("Illinois","Ill.","IL"),
    ("Indiana","Ind.","IN"),
    ("Iowa","Iowa","IA"),
    ("Kansas","Kans.","KS"),
    ("Kentucky","Ky.","KY"),
    ("Louisiana","La.","LA"),
    ("Maine","Maine","ME"),
    ("Maryland","Md.","MD"),
    ("Massachusetts","Mass.","MA"),
    ("Michigan","Mich.","MI"),
    ("Minnesota","Minn.","MN"),
    ("Mississippi","Miss.","MS"),
    ("Missouri","Mo.","MO"),
    ("Montana","Mont.","MT"),
    ("Nebraska","Nebr.","NE"),
    ("Nevada","Nev.","NV"),
    ("New Hampshire","N.H.","NH"),
    ("New Jersey","N.J.","NJ"),
    ("New Mexico","N.M.","NM"),
    ("New York","N.Y.","NY"),
    ("North Carolina","N.C.","NC"),
    ("North Dakota","N.D.","ND"),
    ("Ohio","Ohio","OH"),
    ("Oklahoma","Okla.","OK"),
    ("Oregon","Ore.","OR"),
    ("Pennsylvania","Pa.","PA"),
    ("Rhode Island","R.I.","RI"),
    ("South Carolina","S.C.","SC"),
    ("South Dakota","S.D.","SD"),
    ("Tennessee","Tenn.","TN"),
    ("Texas","Tex.","TX"),
    ("Utah","Utah","UT"),
    ("Vermont","Vt.","VT"),
    ("Virginia","Va.","VA"),
    ("Washington","Wash.","WA"),
    ("West Virginia","W.Va.","WV"),
    ("Wisconsin","Wis.","WI"),
    ("Wyoming","Wyo.","WY"),
]

_STATE_CODE_TO_NAME = {
    code: name for (name, _, code) in _RAW_STATE_ABBREVIATIONS
}

_STATE_NAME_TO_CODE = {
    name: code for (name, _, code) in _RAW_STATE_ABBREVIATIONS
}

# Raw data: https://worldpopulationreview.com/state-rankings/mass-shootings-by-state
_RAW_GV_STATS = [
    # ("fips","state","densityMi","pop2023","pop2022","pop2020","pop2019","pop2010","growthRate","growth","growthSince2010","massShootings","massShootingsPerCapita"),
    ("6","California","258.20877",40223504,39995077,39538223,39309799,37253956,"0.00571",228427,"0.07971",257,0.6389299152057961),
    ("17","Illinois","230.67908",12807072,12808884,12812508,12814324,12830632,"-0.00014",-1812,"-0.00184",209,1.6319108692447422),
    ("12","Florida","416.95573",22359251,22085563,21538187,21264502,18801310,"0.01239",273688,"0.18924",147,0.6574459940540942),
    ("48","Texas","116.16298",30345487,29945493,29145505,28745507,25145561,"0.01336",399994,"0.20679",129,0.4251043985552118),
    ("36","New York","433.90472",20448194,20365879,20201249,20118937,19378102,"0.00404",82315,"0.05522",96,0.4694791139012081),
    ("42","Pennsylvania","292.62222",13092796,13062764,13002700,12972667,12702379,"0.00230",30032,"0.03074",92,0.7026764947685735),
    ("13","Georgia","191.59470",11019186,10916760,10711908,10609487,9687653,"0.00938",102426,"0.13745",89,0.8076821645446407),
    ("22","Louisiana","108.67214",4695071,4682633,4657757,4645314,4533372,"0.00266",12438,"0.03567",87,1.8530071217240378),
    ("47","Tennessee","171.70515",7080262,7023788,6910840,6854371,6346105,"0.00804",56474,"0.11569",84,1.1863967745826356),
    ("39","Ohio","290.70091",11878330,11852036,11799448,11773150,11536504,"0.00222",26294,"0.02963",80,0.6734953482518166),
    ("29","Missouri","90.26083",6204710,6188111,6154913,6138318,5988927,"0.00268",16599,"0.03603",73,1.1765255749261447),
    ("26","Michigan","179.26454",10135438,10116069,10077331,10057961,9883640,"0.00191",19369,"0.02548",66,0.6511805409889538),
    ("34","New Jersey","1283.40005",9438124,9388414,9288994,9239284,8791894,"0.00529",49710,"0.07350",65,0.6886961858098071),
    ("10","Delaware","522.08876",1017551,1008350,989948,980743,897934,"0.00912",9201,"0.13321",58,5.699960002004813),
    ("24","Maryland","648.84362",6298325,6257958,6177224,6136855,5773552,"0.00645",40367,"0.09089",58,0.9208797577133603),
    ("37","North Carolina","220.30026",10710558,10620168,10439388,10348993,9535483,"0.00851",90390,"0.12323",57,0.5321851578601227),
    ("18","Indiana","191.92896",6876047,6845874,6785528,6755359,6483802,"0.00441",30173,"0.06050",54,0.7853349460816658),
    ("51","Virginia","223.36045",8820504,8757467,8631393,8568357,8001024,"0.00720",63037,"0.10242",54,0.6122099145354959),
    ("1","Alabama","100.65438",5097641,5073187,5024279,4999822,4779736,"0.00482",24454,"0.06651",49,0.9612289292243216),
    ("45","South Carolina","175.18855",5266343,5217037,5118425,5069118,4625364,"0.00945",49306,"0.13858",44,0.8354943838637171),
    ("28","Mississippi","63.07084",2959473,2960075,2961279,2961879,2967297,"-0.00020",-602,"-0.00264",34,1.1488531910917923),
    ("21","Kentucky","115.37702",4555777,4539130,4505836,4489190,4339367,"0.00367",16647,"0.04987",28,0.6146042705777741),
    ("4","Arizona","64.96246",7379346,7303398,7151502,7075549,6392017,"0.01040",75948,"0.15446",27,0.3658860825878066),
    ("8","Colorado","57.86332",5997070,5922618,5773714,5699264,5029196,"0.01257",74452,"0.19245",24,0.4001954287677149),
    ("53","Washington","120.37292",7999503,7901429,7705281,7607206,6724540,"0.01241",98074,"0.18960",24,0.30001863865792666),
    ("40","Oklahoma","58.63041",4021753,4000953,3959353,3938551,3751351,"0.00520",20800,"0.07208",22,0.5470251405295153),
    ("27","Minnesota","73.18202",5827265,5787008,5706494,5666238,5303925,"0.00696",40257,"0.09867",21,0.36037489285282204),
    ("5","Arkansas","58.42619",3040207,3030646,3011524,3001967,2915918,"0.00315",9561,"0.04262",19,0.6249574453318475),
    ("9","Connecticut","746.69537",3615499,3612314,3605944,3602762,3574097,"0.00088",3185,"0.01158",19,0.5255152884843834),
    ("20","Kansas","36.24443",2963308,2954832,2937880,2929402,2853118,"0.00287",8476,"0.03862",18,0.6074292648621068),
    ("32","Nevada","29.38425",3225832,3185426,3104614,3064205,2700551,"0.01268",40406,"0.19451",18,0.557995580675001),
    ("25","Massachusetts","919.82103",7174604,7126375,7029917,6981690,6547629,"0.00677",48229,"0.09576",16,0.2230088239016397),
    ("35","New Mexico","17.60148",2135024,2129190,2117522,2111685,2059179,"0.00274",5834,"0.03683",15,0.7025682146898583),
    ("31","Nebraska","26.06024",2002052,1988536,1961504,1947985,1826341,"0.00680",13516,"0.09621",8,0.39959002063882454),
    ("41","Oregon","45.41307",4359110,4318492,4237256,4196636,3831074,"0.00941",40618,"0.13783",7,0.160583238321584),
    ("19","Iowa","57.89018",3233572,3219171,3190369,3175964,3046355,"0.00447",14401,"0.06146",6,0.1855533137966311),
    ("55","Wisconsin","109.96966",5955737,5935064,5893718,5873043,5686986,"0.00348",20673,"0.04726",6,0.10074319937230271),
    ("49","Utah","41.66892",3423935,3373162,3271616,3220842,2763885,"0.01505",50773,"0.23881",5,0.14603080958020523),
    ("44","Rhode Island","1074.29594",1110822,1106341,1097379,1092896,1052567,"0.00405",4481,"0.05535",4,0.360093696379798),
    ("30","Montana","7.64479",1112668,1103187,1084225,1074744,989415,"0.00859",9481,"0.12457",3,0.2696222053658414),
    ("54","West Virginia","73.88019",1775932,1781860,1793716,1799642,1852994,"-0.00333",-5928,"-0.04159",3,0.16892538678282729),
    ("23","Maine","44.50148",1372559,1369159,1362359,1358961,1328361,"0.00248",3400,"0.03327",2,0.14571322617096968),
    ("46","South Dakota","11.98261",908414,901165,886667,879421,814180,"0.00804",7249,"0.11574",2,0.22016393406530504),
    ("2","Alaska","1.29738",740339,738023,733391,731075,710231,"0.00314",2316,"0.04239",1,0.13507325698092362),
    ("50","Vermont","70.33514",648279,646545,643077,641347,625741,"0.00268",1734,"0.03602",1,0.15425457249116506),
    ("15","Hawaii","231.00763",1483762,1474265,1455271,1445774,1360301,"0.00644",9497,"0.09076",0,0),
    ("16","Idaho","23.23926",1920562,1893410,1839106,1811950,1567582,"0.01434",27152,"0.22517",0,0),
    ("33","New Hampshire","155.90830",1395847,1389741,1377529,1371424,1316470,"0.00439",6106,"0.06030",0,0),
    ("38","North Dakota","11.75409",811044,800394,779094,768441,672591,"0.01331",10650,"0.20585",0,0),
    ("56","Wyoming","5.98207",580817,579495,576851,575524,563626,"0.00228",1322,"0.03050",0,0),
]


@dataclasses.dataclass
class GvStats:
    state_name: str
    pop2023: int
    num_mass_shootings: int
    mass_shootings_per_capita: float


# Maps a state name to the state's gun violence stats.
_STATE_NAME_TO_GV_STATS = {
    state_name: GvStats(state_name=state_name, pop2023=pop2023, num_mass_shootings=num_mass_shootings, mass_shootings_per_capita=mass_shootings_per_capita)
    for (_, state_name, _, pop2023, _, _, _, _, _, _, _, num_mass_shootings, mass_shootings_per_capita) in _RAW_GV_STATS
}


# print(_STATE_CODE_TO_COLOR)
# print(len(_STATE_CODE_TO_COLOR))
sorted_by_ms_per_capita = sorted(_STATE_NAME_TO_GV_STATS.values(), key=lambda s: s.mass_shootings_per_capita, reverse=True)
for stats in sorted_by_ms_per_capita:
    code = _STATE_NAME_TO_CODE[stats.state_name]
    color = _STATE_CODE_TO_COLOR[code]
    print(f"{stats.state_name}: {color}, {stats.mass_shootings_per_capita}, {stats.num_mass_shootings}")