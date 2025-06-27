# Test Data

## Generated Test Data Cases

Test cases based on the patent data we have loaded so far.

### I. No Expected Matches (High Precision Test)

#### Test Case 1.1: Completely Unrelated Medical Device
* **User Invention Description:** "A novel surgical instrument designed for laparoscopic prostatectomy, featuring articulating robotic arms with haptic feedback for enhanced precision. The instrument incorporates a disposable cutting head with integrated cautery capabilities and a miniature camera for real-time visualization, allowing for minimally invasive procedures with reduced patient recovery time."
* **Expected Prior Art (and Ranking):** No direct matches are expected. Any results should have very low similarity scores.
* **Rationale:** This describes a highly specialized medical device, distinct from anything in your provided patent abstracts, which lean towards materials, general mechanics, or chemical processes. This tests if your system can correctly identify a lack of relevant prior art.

#### Test Case 1.2: Advanced Space Propulsion
* **User Invention Description:** "An innovative propulsion system for interstellar travel, utilizing a high-energy plasma drive powered by fusion reactions. The system incorporates a magnetic confinement chamber for plasma stability and an advanced heat dissipation mechanism, enabling sustained acceleration over vast distances without reliance on chemical propellants."
* **Expected Prior Art (and Ranking):** No direct matches expected.
* **Rationale:** Like the medical device, this is a distinct and highly specialized field not covered by your dataset.

### II. Single Obvious Match (Basic Relevance Test)

#### Test Case 2.1: Improved Two-Ply Thermal Paper
* **User Invention Description:** "A two-ply thermal paper with enhanced durability and print longevity. This new paper offers improved resistance to fading from environmental exposure, while maintaining the ability for easy separation of the top and base sheets after thermal printing, similar to existing two-ply media."
* **Expected Prior Art (and Ranking):**
    * CA-1327142-C: "Two ply thermal paper and method of making"
    * (All others significantly lower)
* **Rationale:** This directly references "two-ply thermal paper" and its core functionality, making CA-1327142-C the perfect and obvious match. This tests if your `abstract_similarity` and keyword weighting correctly prioritize direct hits.

#### Test Case 2.2: Insulated Drinkware with Dual Openings
* **User Invention Description:** "A vacuum-insulated bottle featuring a broad opening for convenient filling and cleaning, along with an internal, narrow-mouthed liner. This liner extends upwards to facilitate spill-free pouring and optimizes thermal retention, combining the benefits of wide and narrow openings."
* **Expected Prior Art (and Ranking):**
    * US3910441A: "Vacuum Insulated Bottle"
    * US4427123A: "Stainless steel thermos bottle" (Less specific on wide/narrow opening)
    * US6405892B1: "Thermally Insulated Beverage Glass" (Different form factor, but insulated)
* **Rationale:** This invention directly describes the "wide opening vacuum filler" and "narrow mouth opening to the lined interior" features of US3910441A. The other US patents on insulation are related but less specific to the dual-opening design.

### III. Multiple Matches with Clear Ranking (Graded Relevance Test)

#### Test Case 3.1: Enhanced Exhaust Gas Treatment System
* **User Invention Description:** "An exhaust gas treatment system for internal combustion engines, incorporating an improved catalytic converter designed to reduce NOx emissions. The converter has a novel substrate structure with varying channel cross-sections and angled, crossing channels in adjacent layers to enhance catalytic activity and allow for compact design in vehicles."
* **Expected Prior Art (and Ranking):**
    * CA-2128143-C: "Exhaust gas catalytic converter, particularly for motor cars" (Direct match on variable area/shape, angled channels, crossing layers)
    * CA-2709457-C: "Denox of diesel engine exhaust gases using a temperature-controlled precatalyst for providing no2 in accordance with the requirements" (General diesel exhaust NOx reduction, but different mechanism)
    * CA-2778179-C: "System and method for processing an input fuel gas and steam to produce carbon dioxide and an output fuel gas" (Broader gas processing, not specific to exhaust gas catalytic conversion)
    * CA-1136062-A: "Heat-reactivatable adsorbent gas fractionator and process" (Adsorbent based gas separation, general, not catalytic exhaust)
* **Rationale:** CA-2128143-C is an almost perfect match for the specific catalytic converter design features. CA-2709457-C is still highly relevant as it's about NOx reduction in diesel exhaust but uses a different catalytic approach. The others are progressively less relevant, dealing with gas processing in general.

#### Test Case 3.2: Automated Door Mounting System for Vehicles
* **User Invention Description:** "A robotic system for automating the assembly of vehicle doors onto car bodies. The system includes conveyors for precise positioning of the door and body, and multiple robotic arms equipped with sensors for measuring openings and accurately placing the door, all controlled by a central computer for optimized alignment."
* **Expected Prior Art (and Ranking):**
    * CA-1266762-A: "Apparatus for automated mounting of a door or similar closure component within the relative opening formed in a body, in particular an automotive vehicle body" (Direct match on automated door mounting apparatus for vehicles)
    * CA-2075526-C: "Conveyorized vacuum applicator and method therefor" (Shares "conveyorized," "automated," "applying/mounting," "method and apparatus," but different application - PCB lamination. This is your "tricky" case from before.)
    * CA-1265568-A: "Linear stepping motor" (Relates to automated movement/control, but not specific to assembly or doors)
* **Rationale:** CA-1266762-A is an almost exact description of the user invention. CA-2075526-C is a good second-tier match to test your weighting, as it shares several keywords ("conveyorized," "automated," "method and apparatus," "applying") but is in a different domain (PCB lamination). CA-1265568-A is a more general automation component.

### IV. Tricky Cases (Stress Test for Semantic Nuance)

#### Test Case 4.1: Chemical Process for Hydrocarbon Conversion
* **User Invention Description:** "A novel process for converting gaseous hydrocarbon feeds into liquid fuel products, involving a catalytic bed and a cooling mechanism to manage exothermic reactions and separate liquid products in-situ, thereby enhancing yield and preventing catalyst deactivation due to product buildup."
* **Expected Prior Art (and Ranking):**
    * CA-2713874-C: "Method and reactor for the preparation of methanol" (Highly relevant: in-situ separation, liquid cooling, catalyst activity maintenance, specific reactor design for equilibrium reactions)
    * CA-1136062-A: "Heat-reactivatable adsorbent gas fractionator and process" (Less relevant: gas fractionation via adsorption and microwave heating, not catalytic conversion to liquid fuel with in-situ liquid separation for catalyst activity)
    * CA-2027605-C: "Process for treating a spent nickel-based absorbent" (Even less relevant: treating spent absorbent, not a conversion process)
* **Rationale:** This query is designed to hit CA-2713874-C hard because it's a very specific description of a catalytic conversion with in-situ liquid product removal for catalyst maintenance. The other chemical patents, while mentioning "process" or "gas," are semantically distant in their specific mechanisms and goals, testing if your abstract embedding can distinguish this.

#### Test Case 4.2: Flexible Electrical Connector for Modular Devices
* **User Invention Description:** "A flexible electrical connector system designed for modular electronic devices with replaceable components. The connector ensures reliable power and data transfer between detachable modules, allowing for robust yet easily severable connections, particularly useful in consumer electronics with user-serviceable parts."
* **Expected Prior Art (and Ranking):**
    * CA-2540125-C: "Toothbrush with severable electrical connections" (Direct match: "severable electrical connector," "removable/replaceable head," "electrical communication" for elements requiring power)
    * CA-2699970-C: "Internal crosstalk compensation circuit formed on a flexible printed circuit board positioned within a communications outlet, and methods and systems relating to same" (Less relevant: mentions "flexible printed circuit board" and "electrical contacts" but is about crosstalk compensation in network outlets, not modular device connections)
    * CA-2751329-C: "Fiber optic jack and connector" (Less relevant: general connector, but for fiber optics, not electrical power/data in a modular consumer device context)
* **Rationale:** CA-2540125-C is highly specific to the "severable electrical connection" for "removable/replaceable" parts in an "oral care implement" (a consumer electronic device). This tests if your system can find relevant concepts even when the domain (toothbrush vs. general modular device) isn't explicitly mentioned, but the functionality is the same. CA-2699970-C contains "flexible" and "electrical connections" but in a different functional context.