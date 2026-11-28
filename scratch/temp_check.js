
                // Master 28-Brand Formulation Database
    const PRODUCTS = [
      {
            "id": "synogut",
            "title": "SynoGut™",
            "category": "gut",
            "superlative": "🌿 #1 Complete Digestive & Intestinal Microbiome Cleanse",
            "image": "/Imagens_Oficiais/synogut_bottle.png",
            "rating": 4.9,
            "reviews": "2,460+",
            "price": "$49/bottle",
            "originalPrice": "$69",
            "guarantee": "60-Day Guarantee",
            "desc": "Natural blend formulated with Psyllium, Bentonite Clay, Flaxseed, and Probiotics to soothe digestive lining and support regular bowel motility.",
            "showcase": "/go/synogut",
            "review": "/synogut-review/",
            "go": "/go/synogut"
      },
      {
            "id": "nervecalm",
            "title": "NerveCalm™",
            "category": "brain",
            "superlative": "⚡ #1 Peripheral Nerve Repair & Neuropathy Relief",
            "image": "/Imagens_Oficiais/nervecalm_bottle.png",
            "rating": 4.9,
            "reviews": "2,180+",
            "price": "$49/bottle",
            "originalPrice": "$89",
            "guarantee": "90-Day Guarantee",
            "desc": "Targeted botanical nerve formula with Corydalis Yanhusuo, Opuntia, and Marshmallow Root to soothe burning feet and nerve tingling.",
            "showcase": "/go/nervecalm",
            "review": "/nervecalm-review/",
            "go": "/go/nervecalm"
      },
      {
            "id": "colestzen",
            "title": "ColestZen™",
            "category": "heart",
            "superlative": "🫀 #1 Arterial Elasticity & Lipid Clearance",
            "image": "/Imagens_Oficiais/colestzen_bottle.png",
            "rating": 4.9,
            "reviews": "1,940+",
            "price": "$49/bottle",
            "originalPrice": "$99",
            "guarantee": "60-Day Guarantee",
            "desc": "Cardiovascular and lipid balance formula featuring Bergavit, Guggul, and Artichoke to maintain healthy arterial compliance.",
            "showcase": "/go/colestzen",
            "review": "/colestzen-review/",
            "go": "/go/colestzen"
      },
      {
            "id": "vigorsana",
            "title": "VigorSana™",
            "category": "men",
            "superlative": "⚡ #1 Botanical Nitric Oxide & Cellular Vitality",
            "image": "/Imagens_Oficiais/vigorsana_bottle.png",
            "rating": 4.9,
            "reviews": "1,420+",
            "price": "$49/bottle",
            "originalPrice": "$69",
            "guarantee": "60-Day Guarantee",
            "desc": "Advanced botanical nitric oxide and cellular energy formula featuring L-Citrulline, French Maritime Pine Bark, and Maca Root.",
            "showcase": "/go/vigorsana",
            "review": "/vigorsana-review/",
            "go": "/go/vigorsana"
      },
      {
            "id": "livarix",
            "title": "Livarix™",
            "category": "liver",
            "superlative": "🌿 Targeted Hepatic Lipid & Bile Clearance",
            "image": "/Imagens_Oficiais/livarix_bottle.png",
            "rating": 4.9,
            "reviews": "1,840+",
            "price": "$49/bottle",
            "originalPrice": "$99",
            "guarantee": "60-Day Guarantee",
            "desc": "Clinical hepatic support complex engineered to optimize bile acid synthesis, Phase II conjugation, and liver cell regeneration.",
            "showcase": "/go/livarix",
            "review": "/livarix-review/",
            "go": "/go/livarix"
      },
      {
            "id": "nagano",
            "title": "Nagano Lean Body Tonic\u2122",
            "category": "weight",
            "superlative": "\ud83d\udd25 #1 Resting Metabolism Elixir",
            "image": "/showcase/nagano-tonic/images/sigle-btl-new.png",
            "rating": 4.9,
            "reviews": "2,840+",
            "price": "$39/bottle",
            "originalPrice": "$127",
            "guarantee": "180-Day Guarantee",
            "desc": "Authentic Japanese morning tonic with EGCG, Camu Camu, and Ashwagandha to reactivate dormant metabolism.",
            "showcase": "/showcase/nagano-tonic",
            "review": "/nagano-tonic-review",
            "go": "/go/nagano"
      },
      {
            "id": "advanced-joint",
            "title": "Advanced Joint Support\u2122",
            "category": "joints",
            "superlative": "\ud83e\uddb4 Fast Cartilage & Mobility Relief",
            "image": "/Imagens_Oficiais/advanced_joint_single.png",
            "rating": 4.9,
            "reviews": "1,980+",
            "price": "$41.50/bottle",
            "originalPrice": "$79",
            "guarantee": "90-Day Guarantee",
            "desc": "Glucosamine, Chondroitin, MSM, and Boswellia Serrata designed to restore joint fluid and synovial cushion.",
            "showcase": "/showcase/advanced-joint",
            "review": "/advanced-joint-support-report",
            "go": "/go/jointsupport"
      },
      {
            "id": "prodentim",
            "title": "ProDentim\u00ae Oral Health",
            "category": "dental",
            "superlative": "\ud83e\uddb7 3.5B Good Oral Probiotic Chew",
            "image": "/Imagens_Oficiais/prodentim_bottle.png",
            "rating": 4.9,
            "reviews": "3,410+",
            "price": "$49/bottle",
            "originalPrice": "$99",
            "guarantee": "60-Day Guarantee",
            "desc": "Doctor-formulated dissolving probiotic candy that repopulates healthy mouth bacteria for gum integrity and clean breath.",
            "showcase": "/showcase/prodentim",
            "review": "/prodentim-report",
            "go": "/go/prodentim"
      },
      {
            "id": "corevital",
            "title": "CoreVital Burn\u2122",
            "category": "weight",
            "superlative": "\u26a1 Brown Adipose Tissue (BAT) Catalyst",
            "image": "/showcase/corevital/images/bottle-hero.png",
            "rating": 4.8,
            "reviews": "1,450+",
            "price": "$29.90/bottle",
            "originalPrice": "$69",
            "guarantee": "60-Day Guarantee",
            "desc": "Dr. Samir Bute formulation targeting thermogenic brown fat conversion for 24-hour resting caloric expenditure.",
            "showcase": "/go/corevital",
            "review": "/staging/corevital-burn",
            "go": "/go/corevital"
      },
      {
            "id": "ketosana",
            "title": "KetoSana\u00ae US Liquid Drops",
            "category": "weight",
            "superlative": "\ud83d\udca7 2 Fl Oz Liquid Metabolic Drops (US)",
            "image": "/Imagens_Oficiais/ketosana_1_bottle.png",
            "rating": 4.9,
            "reviews": "1,280+",
            "price": "$49/bottle",
            "originalPrice": "$69",
            "guarantee": "60-Day Guarantee",
            "desc": "Zero-calorie sublingual drops with 7 mcg Chromium Picolinate & 200 mg botanical-amino blend shipped from Aurora, CO.",
            "showcase": "/showcase/ketosana",
            "review": "/ketosana-metabolic-report",
            "go": "/go/ketosana"
      },
      {
            "id": "cardioslim",
            "title": "Cardio Slim Tea\u2122",
            "category": "cardio",
            "superlative": "\u2764\ufe0f Arterial Elasticity & Nitric Oxide",
            "image": "/showcase/cardioslim/images/hero-pouches-cutout.png",
            "rating": 4.8,
            "reviews": "1,890+",
            "price": "$49/pouch",
            "originalPrice": "$89",
            "guarantee": "60-Day Guarantee",
            "desc": "Physician-engineered herbal infusion supporting endothelial nitric oxide, homocysteine balance, and light stamina.",
            "showcase": "/showcase/cardioslim",
            "review": "/cardioslim-tea-cardio-support-report",
            "go": "/go/cardioslim"
      },
      {
            "id": "sugar-defender",
            "title": "Sugar Defender\u00ae",
            "category": "sugar",
            "superlative": "\ud83e\ude78 24-Herb Liquid Glycemic Dropper",
            "image": "/Imagens_Oficiais/sugar_defender_bottle.png",
            "rating": 4.9,
            "reviews": "2,950+",
            "price": "$49/bottle",
            "originalPrice": "$79",
            "guarantee": "60-Day Guarantee",
            "desc": "Eleuthero, Coleus, and Maca liquid dropper preventing post-meal sugar crashes and afternoon energy slumps.",
            "showcase": "/showcase/sugar-defender",
            "review": "/sugar-defender-guide",
            "go": "/go/sugardefender"
      },
      {
            "id": "cleansesana",
            "title": "CleanseSana\u00ae Colon Cleanse",
            "category": "gut",
            "superlative": "\ud83c\udf3f 15-Day Digestive & Bloating Flush",
            "image": "/Imagens_Oficiais/cleansesana_single_bottle.png",
            "rating": 4.8,
            "reviews": "1,670+",
            "price": "$49/bottle",
            "originalPrice": "$79",
            "guarantee": "60-Day Guarantee",
            "desc": "Psyllium husk, Cascara Sagrada, and Senna leaf facilitating gentle waste clearance and microbiome renewal.",
            "showcase": "/showcase/cleansesana",
            "review": "/cleansesana-gut-reboot",
            "go": "/go/cleansesana"
      },
      {
            "id": "advanced-amino",
            "title": "Advanced Amino Formula\u2122",
            "category": "longevity",
            "superlative": "\ud83d\udcaa 8 Essential Aminos (99% Protein Synthesis)",
            "image": "/showcase/advanced-amino/images/hero-bottles.png",
            "rating": 4.9,
            "reviews": "2,120+",
            "price": "$41.50/bottle",
            "originalPrice": "$79",
            "guarantee": "90-Day Guarantee",
            "desc": "Perfect ratio of crystalline essential amino acids supporting lean muscle, cellular longevity, and cartilage repair.",
            "showcase": "/showcase/advanced-amino",
            "review": "/advanced-amino-formula-report",
            "go": "/go/amino"
      },
      {
            "id": "collagen",
            "title": "Advanced Collagen PLUS\u2122",
            "category": "longevity",
            "superlative": "\u2728 Multi-Collagen Types I, II, III, V, X",
            "image": "/showcase/advanced-collagen/images/hero-collagen-pouches.png",
            "rating": 4.9,
            "reviews": "1,520+",
            "price": "$41.50/pouch",
            "originalPrice": "$79",
            "guarantee": "90-Day Guarantee",
            "desc": "Multi-collagen peptide powder with hyaluronic acid and vitamin C for youthful skin, hair, and cartilage cushion.",
            "showcase": "/showcase/advanced-collagen",
            "review": "/advanced-collagen-plus-report",
            "go": "/go/collagen"
      },
      {
            "id": "memory",
            "title": "Advanced Memory Formula\u2122",
            "category": "brain",
            "superlative": "\ud83e\udde0 Cognitive Focus & Neurogenesis",
            "image": "/showcase/advanced-memory/images/hero-bottles.png",
            "rating": 4.8,
            "reviews": "1,290+",
            "price": "$41.50/bottle",
            "originalPrice": "$69",
            "guarantee": "90-Day Guarantee",
            "desc": "Luteolin, Bacopa Monnieri, Ginkgo Biloba, and NeuroFactor\u2122 supporting brain neurogenesis and fast recall.",
            "showcase": "/showcase/advanced-memory",
            "review": "/advanced-memory-formula-guide",
            "go": "/go/memory"
      },
      {
            "id": "circo2",
            "title": "CirCO2\u00ae Nitric Oxide",
            "category": "cardio",
            "superlative": "\u2764\ufe0f Fast-Acting Dissolving Lozenge",
            "image": "/showcase/circo2/images/circo2-box.png",
            "rating": 4.8,
            "reviews": "1,750+",
            "price": "$41.50/box",
            "originalPrice": "$79",
            "guarantee": "90-Day Guarantee",
            "desc": "Dissolving lozenge delivering nitric oxide to support healthy arterial flow, stamina, and oxygen delivery.",
            "showcase": "/showcase/circo2",
            "review": "/circo2-nitric-oxide-report",
            "go": "/go/circo2"
      },
      {
            "id": "audifort",
            "title": "Audifort\u2122 Ear Support",
            "category": "brain",
            "superlative": "\ud83d\udc42 Auditory Nerve & Ringing Defense",
            "image": "/Imagens_Oficiais/audifort_bottle.png",
            "rating": 4.7,
            "reviews": "980+",
            "price": "$49/bottle",
            "originalPrice": "$79",
            "guarantee": "60-Day Guarantee",
            "desc": "Botanical and micronutrient complex supporting delicate auditory hair cells and healthy microcirculation.",
            "showcase": "/showcase/audifort",
            "review": "/audifort-hearing-support-report",
            "go": "/go/audifort"
      },
      {
            "id": "femicore",
            "title": "FemiCore\u2122 Pelvic Health",
            "category": "longevity",
            "superlative": "\ud83c\udf38 Pelvic Tone & Bladder Confidence",
            "image": "/Imagens_Oficiais/femicore_bottle.png",
            "rating": 4.8,
            "reviews": "1,140+",
            "price": "$49/bottle",
            "originalPrice": "$79",
            "guarantee": "60-Day Guarantee",
            "desc": "Targeted herbal formulation supporting bladder muscle elasticity, pelvic floor integrity, and restful uninterrupted nights.",
            "showcase": "/showcase/femicore",
            "review": "/femicore-pelvic-health-report",
            "go": "/go/femicore"
      },
      {
            "id": "neotonics",
            "title": "Neotonics\u00ae Gut & Skin",
            "category": "longevity",
            "superlative": "\u2728 500M Probiotic Skin Turnover Gummy",
            "image": "/Imagens_Oficiais/neotonics_bottle.png",
            "rating": 4.9,
            "reviews": "2,380+",
            "price": "$49/bottle",
            "originalPrice": "$99",
            "guarantee": "60-Day Guarantee",
            "desc": "Bacillus coagulans and Babchi gummies revitalizing cellular skin turnover rate through the gut-skin axis.",
            "showcase": "/showcase/neotonics",
            "review": "/neotonics-skin-gut-report",
            "go": "/go/neotonics"
      },
      {
            "id": "lymphtonic",
            "title": "LymphTonic\u2122 Drainage",
            "category": "gut",
            "superlative": "\ud83d\udca7 Lymphatic Fluid & Swelling Relief",
            "image": "/Imagens_Oficiais/lymphtonic_bottles.png",
            "rating": 4.7,
            "reviews": "820+",
            "price": "$49/bottle",
            "originalPrice": "$79",
            "guarantee": "60-Day Guarantee",
            "desc": "Cleavers, Burdock Root, and Red Clover liquid tincture promoting lymphatic circulation and natural fluid drainage.",
            "showcase": "/showcase/lymphtonic",
            "review": "/lymphtonic-drainage-report",
            "go": "/go/lymphtonic"
      },
      {
            "id": "visiflora",
            "title": "VisiFlora\u00ae Eye & Vision",
            "category": "longevity",
            "superlative": "\ud83d\udc41\ufe0f Macular Pigment & Blue Light Shield",
            "image": "/Imagens_Oficiais/visiflora_bottle.png",
            "rating": 4.7,
            "reviews": "1,040+",
            "price": "$49/bottle",
            "originalPrice": "$89",
            "guarantee": "60-Day Guarantee",
            "desc": "Lutein, Zeaxanthin, and Bilberry anthocyanins protecting delicate retina cells and supporting sharp visual contrast.",
            "showcase": "/showcase/visiflora",
            "review": "/visiflora-vision-report",
            "go": "/go/visiflora"
      },
      {
            "id": "neurovera",
            "title": "NeuroVera\u2122 Nerve Health",
            "category": "brain",
            "superlative": "\u26a1 Peripheral Nerve Comfort & Myelin",
            "image": "/Imagens_Oficiais/neurovera_bottle.png",
            "rating": 4.7,
            "reviews": "1,150+",
            "price": "$49/bottle",
            "originalPrice": "$79",
            "guarantee": "60-Day Guarantee",
            "desc": "Targeted botanical formula soothing tingling sensations and supporting peripheral nerve myelin sheath protection.",
            "showcase": "/showcase/neurovera",
            "review": "/neurovera-brain-clarity-report",
            "go": "/go/neurovera"
      },
      {
            "id": "phytomem",
            "title": "PhytoMem\u2122 Cognition",
            "category": "brain",
            "superlative": "\ud83e\udde0 Focus, Brain Fog & Acetylcholine",
            "image": "/Imagens_Oficiais/phytomem_bottle.png",
            "rating": 4.7,
            "reviews": "890+",
            "price": "$49/bottle",
            "originalPrice": "$79",
            "guarantee": "60-Day Guarantee",
            "desc": "Natural nootropic compounds supporting neurotransmitter synthesis, mental clarity, and memory preservation.",
            "showcase": "/showcase/phytomem",
            "review": "/phytomem-memory-formula-report",
            "go": "/go/phytomem"
      },
      {
            "id": "joint-eternal",
            "title": "Joint Eternal\u2122",
            "category": "joints",
            "superlative": "\ud83e\uddb4 Synovial Lubrication & Morning Ease",
            "image": "/Imagens_Oficiais/joint_eternal_cutout.png",
            "rating": 4.7,
            "reviews": "1,210+",
            "price": "$49/bottle",
            "originalPrice": "$79",
            "guarantee": "60-Day Guarantee",
            "desc": "Natural joint comfort blend supporting synovial fluid volume, joint cushion, and daily morning flexibility.",
            "showcase": "/showcase/joint-eternal",
            "review": "/joint-eternal-mobility-report",
            "go": "/go/jointeternal"
      },
      {
            "id": "prostavive",
            "title": "ProstaVive\u2122 Men's Health",
            "category": "longevity",
            "superlative": "\ud83e\uddd4 Prostate Comfort & Strong Stream",
            "image": "/Imagens_Oficiais/prostavive_bottles.png",
            "rating": 4.8,
            "reviews": "1,630+",
            "price": "$49/bottle",
            "originalPrice": "$89",
            "guarantee": "60-Day Guarantee",
            "desc": "Nutrient complex supporting normal prostate volume, bladder emptying, and restful night sleep for men.",
            "showcase": "/showcase/prostavive",
            "review": "/prostavive-prostate-health-report",
            "go": "/go/prostavive"
      },
      {
            "id": "slimming-tea",
            "title": "All Day Slimming Tea\u00ae",
            "category": "weight",
            "superlative": "\ud83c\udf75 2-Stage Morning & Evening Detox Tea",
            "image": "/Imagens_Oficiais/all_day_slimming_tea_bundles.png",
            "rating": 4.8,
            "reviews": "1,980+",
            "price": "$49/pouch",
            "originalPrice": "$79",
            "guarantee": "60-Day Guarantee",
            "desc": "Two-stage day and night herbal tea blend supporting resting metabolism and restorative sleep.",
            "showcase": "/showcase/all-day-slimming-tea",
            "review": "/all-day-slimming-tea-report",
            "go": "/go/slimmingtea"
      },
      {
            "id": "spartamax",
            "title": "SpartaMax\u2122 Male Vitality",
            "category": "longevity",
            "superlative": "\u26a1 Stamina, Vitality & Performance",
            "image": "/Imagens_Oficiais/spartamax_bottle.png",
            "rating": 4.7,
            "reviews": "1,080+",
            "price": "$49/bottle",
            "originalPrice": "$89",
            "guarantee": "60-Day Guarantee",
            "desc": "Herbal adaptogen blend supporting healthy testosterone conversion, stamina, and drive.",
            "showcase": "/showcase/spartamax",
            "review": "/spartamax-vitality-gummies-report",
            "go": "/go/spartamax"
      },
      {
            "id": "fimavyn",
            "title": "Fimavyn\u2122 Metabolic Drops",
            "category": "weight",
            "superlative": "\ud83d\udca7 Sublingual Metabolic Activation Drops",
            "image": "/Imagens_Oficiais/fimavyn_bottle_studio.jpg",
            "rating": 4.7,
            "reviews": "950+",
            "price": "$49/bottle",
            "originalPrice": "$79",
            "guarantee": "60-Day Guarantee",
            "desc": "Sublingual liquid botanical drops designed for rapid cellular absorption and natural appetite control.",
            "showcase": "/showcase/fimavyn",
            "review": "/fimavyn-metabolic-activation-report",
            "go": "/go/fimavyn"
      },
      {
            "id": "glucotrust",
            "title": "GlucoTrust\u2122 Glucose Support",
            "category": "sugar",
            "superlative": "\ud83e\ude78 Deep Sleep & Overnight Glucose Balance",
            "image": "/Imagens_Oficiais/glucotrust_german_bottles.png",
            "rating": 4.7,
            "reviews": "1,420+",
            "price": "$49/bottle",
            "originalPrice": "$89",
            "guarantee": "60-Day Guarantee",
            "desc": "Gymnema Sylvestre, Cinnamon, and Biotin supporting healthy overnight glucose balance and deep rest.",
            "showcase": "/showcase/glucotrust",
            "review": "/glucotrust-blutzucker-bericht",
            "go": "/go/glucotrust"
      },
      {
            "id": "javaburn",
            "title": "Java Burn\u2122 Coffee Booster",
            "category": "weight",
            "superlative": "\u2615 10-Second Morning Coffee Packet",
            "image": "/Imagens_Oficiais/javaburn_bottles.png",
            "rating": 4.7,
            "reviews": "2,240+",
            "price": "$39/pouch",
            "originalPrice": "$69",
            "guarantee": "60-Day Guarantee",
            "desc": "Tasteless instant-dissolve morning coffee packet with green tea EGCG and chromium to boost resting metabolic rate.",
            "showcase": "/showcase/java-burn",
            "review": "/java-burn-coffee-ritual-report",
            "go": "/go/javaburn"
      },
      {
            "id": "kerassentials",
            "title": "Kerassentials® Nail & Skin Oil",
            "category": "longevity",
            "superlative": "🌿 Doctor-Formulated Antifungal Oil",
            "image": "/Imagens_Oficiais/kerassentials_bottle.png",
            "rating": 4.9,
            "reviews": "2,190+",
            "price": "$49/bottle",
            "originalPrice": "$99",
            "guarantee": "60-Day Guarantee",
            "desc": "Doctor-formulated botanical oil with Lavender, Tea Tree, Flaxseed, and Undecylenic Acid to eliminate fungal resistance and restore healthy pink nails.",
            "showcase": "/showcase/kerassentials",
            "review": "/kerassentials-nail-fungus-report",
            "go": "/go/kerassentials"
      },
      {
            "id": "nanodefense",
            "title": "NanoDefense Pro™ Nanotech Drops",
            "category": "longevity",
            "superlative": "🔬 1000x Smaller Cellular Penetration",
            "image": "/Imagens_Oficiais/nanodefense_bottle.png",
            "rating": 4.9,
            "reviews": "1,840+",
            "price": "$49/bottle",
            "originalPrice": "$99",
            "guarantee": "60-Day Guarantee",
            "desc": "Proprietary nanotechnology drops with Nano-Silver, Nano-Curcumin, and Luteolin penetrating deep beneath the keratin layer for cellular nail and skin renewal.",
            "showcase": "/showcase/nanodefense",
            "review": "/nanodefense-pro-nanotechnology-report",
            "go": "/go/nanodefensepro"
      },
      {
            "id": "synaptigen",
            "title": "Synaptigen™ Cognitive Clarity",
            "category": "brain",
            "superlative": "🧠 Clears Neural Sugar & Synapse Shield",
            "image": "/Imagens_Oficiais/synaptigen_bottles.png",
            "rating": 4.9,
            "reviews": "12,640+",
            "price": "$49/bottle",
            "originalPrice": "$99",
            "guarantee": "180-Day Guarantee",
            "desc": "Neuro-symbiotic chewable tablets with L. Paracasei, L. Reuteri, and Inulin clearing neural sugar buildup for sharp memory and mental agility.",
            "showcase": "/showcase/synaptigen",
            "review": "/synaptigen-memory-formula-report",
            "go": "/go/synaptigen"
      },
      {
            "id": "metanail",
            "title": "Metanail Complex™ 20-in-1",
            "category": "longevity",
            "superlative": "🌿 20-in-1 Dual Action Nail & Feet",
            "image": "/Imagens_Oficiais/metanail_bundle.png",
            "rating": 4.92,
            "reviews": "18,430+",
            "price": "$49/bottle",
            "originalPrice": "$99",
            "guarantee": "60-Day Guarantee",
            "desc": "20-in-1 essential formula combining topical Serum Pro with 14 kDa protein and Total Cleanse to eliminate stubborn fungal discoloration.",
            "showcase": "/showcase/metanail",
            "review": "/metanail-complex-nail-fungus-report",
            "go": "/go/metanail"
      },
      {
            "id": "jointgenesis",
            "title": "BioDynamix Joint Genesis™",
            "category": "joints",
            "superlative": "🦴 Synovial Jelly & Mobilee® 10x",
            "image": "/Imagens_Oficiais/jointgenesis_ingredients.png",
            "rating": 4.9,
            "reviews": "22,450+",
            "price": "$39/bottle",
            "originalPrice": "$99",
            "guarantee": "180-Day Guarantee",
            "desc": "Doctor-formulated with patented Mobilee® to multiply synovial fluid hyaluronan by 10x, cushioning joints and ending bone-on-bone friction.",
            "showcase": "/showcase/jointgenesis",
            "review": "/joint-genesis-synovial-fluid-report",
            "go": "/go/jointgenesis"
      },
      {
            "id": "synevra",
            "title": "Synevra Lift & Lock System",
            "category": "longevity",
            "superlative": "✨ Swiss Peptide Lift & Lock",
            "image": "/Imagens_Oficiais/synevra_kit.png",
            "rating": 4.9,
            "reviews": "19,420+",
            "price": "$49/bottle",
            "originalPrice": "$99",
            "guarantee": "60-Day Guarantee",
            "desc": "Swiss biomimetic SYN-AKE® dipeptide dual-action formula relaxes facial micro-contractions and smooths deep expression lines.",
            "showcase": "/showcase/synevra",
            "review": "/synevra-lift-and-lock-report",
            "go": "/go/synevra"
      },
      {
            "id": "nitricboost",
            "title": "Nitric Boost Ultra™",
            "category": "men",
            "superlative": "⚡ #1 Nitric Oxide & cGMP Formula",
            "image": "/Imagens_Oficiais/nitricboost_jar.png",
            "rating": 4.9,
            "reviews": "24,680+",
            "price": "$49/jar",
            "originalPrice": "$199",
            "guarantee": "60-Day Guarantee",
            "desc": "8-active powder formula with Beet Root, L-Arginine, and Icariin to ignite Nitric Oxide and protect cGMP for firm erections.",
            "showcase": "/showcase/nitricboost",
            "review": "/nitric-boost-ultra-erection-formula-report",
            "go": "/go/nitricboost"
      },
      {
            "id": "livpure",
            "title": "Liv Pure™",
            "category": "weight",
            "superlative": "🌿 Liver Purification & Fat Burning",
            "image": "/Imagens_Oficiais/livpure_bottle.png",
            "rating": 4.9,
            "reviews": "32,800+",
            "price": "$49/bottle",
            "originalPrice": "$199",
            "guarantee": "60-Day Guarantee",
            "desc": "10 Mediterranean super-nutrients across dual purification and fat-burning complexes to burn calories up to 14x faster.",
            "showcase": "/showcase/livpure",
            "review": "/liv-pure-liver-fat-burning-report",
            "go": "/go/livpure"
      },
      {
            "id": "dentabiome",
            "title": "DentaBiome™",
            "category": "dental",
            "superlative": "🦷 #1 Oral Postbiotic Solution",
            "image": "/Imagens_Oficiais/dentabiome_bottle.png",
            "rating": 4.9,
            "reviews": "27,450+",
            "price": "$49/bottle",
            "originalPrice": "$199",
            "guarantee": "60-Day Guarantee",
            "desc": "World's 1st chewable oral postbiotic formula with Dual-Strain L. Plantarum, BioFresh™, and Purple Carrot to shatter the FabM acid-lock.",
            "showcase": "/showcase/dentabiome",
            "review": "/dentabiome-oral-postbiotic-report",
            "go": "/go/dentabiome"
      },
      {
            "id": "yusleep",
            "title": "Yu Sleep™ Deep Rest",
            "category": "longevity",
            "superlative": "🌙 #1 Tart Cherry & GLP-1 Reset",
            "image": "/Imagens_Oficiais/yusleep_bottle.png",
            "rating": 4.9,
            "reviews": "19,420+",
            "price": "$39/bottle",
            "originalPrice": "$99",
            "guarantee": "60-Day Guarantee",
            "desc": "Doctor-formulated liquid sublingual nano-formula with Montmorency tart cherry, magnesium glycinate, and GABA to stop 3 AM awakenings.",
            "showcase": "/showcase/yusleep",
            "review": "/yusleep-deep-rest-report",
            "go": "/go/yusleep"
      },
      {
            "id": "primebiome",
            "title": "PrimeBiome™ Gut & Skin",
            "category": "longevity",
            "superlative": "🌿 #1 Gut-Skin Axis Probiotic Gummies",
            "image": "/Imagens_Oficiais/primebiome_bottle.png",
            "rating": 4.9,
            "reviews": "22,180+",
            "price": "$49/bottle",
            "originalPrice": "$179",
            "guarantee": "60-Day Guarantee",
            "desc": "Doctor-formulated chewable probiotic gummies with Bacillus Coagulans, Babchi extract, and inulin to heal gut dysbiosis and smooth aging skin.",
            "showcase": "/showcase/primebiome",
            "review": "/primebiome-gut-skin-axis-report",
            "go": "/go/primebiome"
      }
];

    function renderProducts(list) {
      const grid = document.getElementById('products-grid');
      if (!grid) return;
      grid.innerHTML = '';

      if (list.length === 0) {
        grid.innerHTML = `
          <div class="col-span-full py-12 text-center text-slate-500">
            <i class="fa-solid fa-flask-vial text-3xl text-slate-300 mb-3 block"></i>
            <p class="font-bold">No formulations matched your search.</p>
            <button onclick="filterCategory('all')" class="mt-3 text-xs text-emerald-700 underline font-bold">Reset filters & view all 44 brands</button>
          </div>
        `;
        return;
      }

      list.forEach(p => {
        const offerUrl = p.go || p.showcase;
        const reviewUrl = p.review;
        const card = document.createElement('div');
        card.className = "product-card bg-white rounded-2xl border border-slate-200/90 shadow-sm hover:shadow-xl transition-all p-5 flex flex-col justify-between";
        card.setAttribute('data-category', p.category);
        card.setAttribute('data-id', p.id);
        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="text-[10px] font-black uppercase tracking-wider text-slate-700 bg-slate-100 px-2.5 py-0.5 rounded-full border border-slate-200 truncate max-w-[200px]">
                ${p.superlative}
              </span>
              <span class="text-[11px] font-extrabold text-amber-500">★ ${p.rating}</span>
            </div>

            <div class="py-4 flex items-center justify-center">
              <a href="${showcaseUrl}" target="_blank" rel="noopener" class="block group-hover:scale-105 transition-transform">
                <img src="${p.image}" alt="${p.title}" class="product-img h-36 object-contain drop-shadow" loading="lazy" />
              </a>
            </div>

            <h3 class="font-black text-sm text-slate-900 font-serif leading-tight mt-1">
              <a href="${showcaseUrl}" target="_blank" rel="noopener" class="hover:text-emerald-700 transition">
                ${p.title}
              </a>
            </h3>
            <p class="text-[11px] text-slate-500 mt-1 line-clamp-2">${p.desc}</p>
          </div>

          <div class="mt-4 pt-3 border-t border-slate-100">
            <div class="flex items-baseline justify-between mb-3">
              <div>
                <span class="text-base font-black text-slate-900">${p.price}</span>
                <span class="text-xs text-slate-400 line-through ml-1">${p.originalPrice}</span>
              </div>
              <span class="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">${p.guarantee}</span>
            </div>

            <div class="space-y-2">
              <a href="${offerUrl}" target="_blank" rel="noopener sponsored" class="block w-full text-center bg-[#0e5e43] hover:bg-[#09422f] text-white font-extrabold text-xs py-2.5 px-3 rounded-xl shadow-sm transition transform hover:-translate-y-0.5">
                Check Official Offer &rarr;
              </a>
              <a href="${reviewUrl}" target="_blank" rel="noopener" class="block w-full text-center bg-slate-50 hover:bg-slate-100 text-slate-600 font-bold text-[11px] py-1.5 rounded-lg border border-slate-200 transition">
                Read Formulation Audit
              </a>
            </div>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    function filterCategory(cat) {
      document.querySelectorAll('.cat-pill').forEach(btn => {
        btn.classList.remove('active', 'bg-[#0e5e43]', 'text-white', 'border-emerald-700');
        btn.classList.add('bg-white', 'text-slate-600', 'border-slate-200');
      });

      const clickedBtn = (typeof event !== 'undefined' && event) ? event.target.closest('button') : null;
      if (clickedBtn && clickedBtn.classList.contains('cat-pill')) {
        clickedBtn.classList.add('active', 'bg-[#0e5e43]', 'text-white', 'border-emerald-700');
        clickedBtn.classList.remove('bg-white', 'text-slate-600', 'border-slate-200');
      }

      if (cat === 'all') {
        renderProducts(PRODUCTS);
      } else {
        const filtered = PRODUCTS.filter(p => p.category === cat);
        renderProducts(filtered);
      }

      const catalogSec = document.getElementById('catalog');
      if (catalogSec && !clickedBtn?.classList.contains('cat-pill')) {
        catalogSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }

    function searchProducts() {
      const q = document.getElementById('product-search').value.toLowerCase().trim();
      if (!q) {
        renderProducts(PRODUCTS);
        return;
      }
      const filtered = PRODUCTS.filter(p => 
        p.title.toLowerCase().includes(q) || 
        p.desc.toLowerCase().includes(q) || 
        p.superlative.toLowerCase().includes(q)
      );
      renderProducts(filtered);
    }

    // Initialize immediately and on DOMContentLoaded
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        renderProducts(PRODUCTS);
      });
    } else {
      renderProducts(PRODUCTS);
    }




    // Mobile Menu Toggle
    (function initMobileMenu() {
      const btn = document.getElementById('mobileMenuBtn');
      const drawer = document.getElementById('mobileMenuDrawer');
      const icon = document.getElementById('mobileMenuIcon');
      if (!btn || !drawer || !icon) return;

      btn.addEventListener('click', function() {
        const isExpanded = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!isExpanded));
        if (isExpanded) {
          drawer.classList.add('hidden');
          icon.classList.remove('fa-xmark');
          icon.classList.add('fa-bars');
        } else {
          drawer.classList.remove('hidden');
          icon.classList.remove('fa-bars');
          icon.classList.add('fa-xmark');
        }
      });

      document.querySelectorAll('.mobile-nav-link').forEach(function(link) {
        link.addEventListener('click', function() {
          drawer.classList.add('hidden');
          btn.setAttribute('aria-expanded', 'false');
          icon.classList.remove('fa-xmark');
          icon.classList.add('fa-bars');
        });
      });
    })();
  