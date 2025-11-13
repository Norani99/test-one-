"""
Enhanced Circular Economy Simulation with Cannibalization Effects
Tests how product longevity and reconditioning quality impact sales and revenue
"""

from mesa import Agent, Model
from mesa import DataCollector
import random
import numpy as np
from enum import Enum


class ProductState(Enum):
    """States a product can be in"""
    NEW = "new"
    USED = "used"
    RECYCLED = "recycled"
    REMANUFACTURED = "remanufactured"
    WASTE = "waste"


class ProductQuality(Enum):
    """Quality levels affecting product longevity"""
    LOW = "low"  # Planned obsolescence
    MEDIUM = "medium"  # Standard quality
    HIGH = "high"  # Durable, long-lasting


class Product:
    """Represents a product with quality and longevity attributes"""
    def __init__(self, product_id, state=ProductState.NEW, co2_footprint=0, quality=ProductQuality.MEDIUM):
        self.id = product_id
        self.state = state
        self.co2_footprint = co2_footprint
        self.quality = quality
        self.lifetime = 0

        # Quality affects max lifetime (CANNIBALIZATION FACTOR)
        base_lifetime = random.randint(10, 20)
        if quality == ProductQuality.LOW:
            self.max_lifetime = int(base_lifetime * 0.5)  # 50% shorter life
        elif quality == ProductQuality.MEDIUM:
            self.max_lifetime = base_lifetime
        else:  # HIGH quality
            self.max_lifetime = int(base_lifetime * 2.0)  # 2x longer life

    def use(self):
        """Use the product, increasing its lifetime"""
        self.lifetime += 1
        self.co2_footprint += 0.1  # CO2 from usage
        return self.lifetime >= self.max_lifetime


class UserAgent(Agent):
    """Agent representing a consumer"""

    def __init__(self, model):
        super().__init__(model)
        self.products = []
        self.money = random.uniform(1000, 5000)
        self.co2_tax_paid = 0
        self.preference_new = random.uniform(0.3, 0.7)
        self.total_spent = 0

    def step(self):
        """Execute one step"""
        # Use existing products
        for product in self.products[:]:
            is_worn = product.use()
            if is_worn:
                self.dispose_product(product)

        # Consider buying if have few products
        if len(self.products) < 3 and random.random() < 0.3:
            self.buy_product()

    def buy_product(self):
        """Buy a new or remanufactured product"""
        available_remanufactured = self.model.remanufactured_inventory

        if available_remanufactured > 0 and random.random() > self.preference_new:
            # Buy remanufactured
            product = Product(
                self.model.next_product_id(),
                state=ProductState.REMANUFACTURED,
                co2_footprint=5,
                quality=self.model.reconditioning_quality
            )
            self.model.remanufactured_inventory -= 1
            base_cost = 80
            co2_tax = product.co2_footprint * self.model.co2_tax_rate
        else:
            # Buy new
            product = Product(
                self.model.next_product_id(),
                state=ProductState.NEW,
                co2_footprint=20,
                quality=self.model.product_quality
            )
            base_cost = 100
            co2_tax = product.co2_footprint * self.model.co2_tax_rate

        total_cost = base_cost + co2_tax
        if self.money >= total_cost:
            self.money -= total_cost
            self.co2_tax_paid += co2_tax
            self.total_spent += total_cost
            self.products.append(product)
            self.model.total_co2_tax_collected += co2_tax
            self.model.total_revenue += base_cost
            self.model.products_sold += 1

    def dispose_product(self, product):
        """Dispose of a used product"""
        self.products.remove(product)
        product.state = ProductState.USED

        if random.random() < self.model.recycling_rate:
            self.model.recycling_queue.append(product)
        else:
            self.model.waste_generated += 1
            self.model.total_co2 += 10


class RecyclingAgent(Agent):
    """Recycling facility agent"""

    def __init__(self, model):
        super().__init__(model)
        self.capacity = random.randint(5, 15)
        self.efficiency = random.uniform(0.7, 0.95)
        self.products_recycled = 0

    def step(self):
        """Process products from recycling queue"""
        processed = 0
        while processed < self.capacity and self.model.recycling_queue:
            product = self.model.recycling_queue.pop(0)

            co2_from_recycling = 2
            self.model.total_co2 += co2_from_recycling

            if random.random() < self.efficiency:
                product.state = ProductState.RECYCLED
                product.co2_footprint += co2_from_recycling
                self.model.recycled_materials.append(product)
                self.products_recycled += 1
            else:
                self.model.waste_generated += 1
                self.model.total_co2 += 5

            processed += 1


class RemanufacturingAgent(Agent):
    """Remanufacturing facility agent"""

    def __init__(self, model):
        super().__init__(model)
        self.capacity = random.randint(3, 10)
        self.products_remanufactured = 0

    def step(self):
        """Remanufacture products from recycled materials"""
        processed = 0
        while processed < self.capacity and self.model.recycled_materials:
            product = self.model.recycled_materials.pop(0)

            co2_from_remanufacturing = 3
            self.model.total_co2 += co2_from_remanufacturing

            product.state = ProductState.REMANUFACTURED
            product.co2_footprint = 5
            product.lifetime = 0

            # Reconditioning quality affects remanufactured product lifetime
            product.quality = self.model.reconditioning_quality
            base_lifetime = random.randint(8, 18)
            if product.quality == ProductQuality.LOW:
                product.max_lifetime = int(base_lifetime * 0.5)
            elif product.quality == ProductQuality.MEDIUM:
                product.max_lifetime = base_lifetime
            else:
                product.max_lifetime = int(base_lifetime * 2.0)

            self.model.remanufactured_inventory += 1
            self.products_remanufactured += 1
            processed += 1


class CircularEconomyModelWithCannibalization(Model):
    """Enhanced model with cannibalization effects"""

    def __init__(
        self,
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.5,
        recycling_rate=0.7,
        product_quality=ProductQuality.MEDIUM,
        reconditioning_quality=ProductQuality.MEDIUM
    ):
        super().__init__()
        self.num_users = n_users
        self.num_recyclers = n_recyclers
        self.num_remanufacturers = n_remanufacturers
        self.co2_tax_rate = co2_tax_rate
        self.recycling_rate = recycling_rate
        self.product_quality = product_quality
        self.reconditioning_quality = reconditioning_quality

        # Model state variables
        self.recycling_queue = []
        self.recycled_materials = []
        self.remanufactured_inventory = 0
        self.total_co2 = 0
        self.total_co2_tax_collected = 0
        self.waste_generated = 0
        self.products_sold = 0
        self.total_revenue = 0  # Track revenue (CANNIBALIZATION METRIC)
        self._product_counter = 0
        self._steps = 0  # Track number of steps

        # Store agents
        self.user_agents = []
        self.recycling_agents = []
        self.remanufacturing_agents = []

        # Create agents
        for i in range(self.num_users):
            agent = UserAgent(self)
            self.user_agents.append(agent)

        for i in range(self.num_recyclers):
            agent = RecyclingAgent(self)
            self.recycling_agents.append(agent)

        for i in range(self.num_remanufacturers):
            agent = RemanufacturingAgent(self)
            self.remanufacturing_agents.append(agent)

        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "Total CO2": "total_co2",
                "CO2 Tax Collected": "total_co2_tax_collected",
                "Waste Generated": "waste_generated",
                "Products Sold": "products_sold",
                "Total Revenue": "total_revenue",  # NEW: Revenue tracking
                "Revenue per Step": self.revenue_per_step,  # NEW: Sales velocity
                "Remanufactured Inventory": "remanufactured_inventory",
                "Total Products in Use": self.count_products_in_use,
            }
        )

    def revenue_per_step(self):
        """Calculate average revenue per step (sales velocity)"""
        if self._steps > 0:
            return self.total_revenue / self._steps
        return 0

    def next_product_id(self):
        """Generate unique product ID"""
        self._product_counter += 1
        return self._product_counter

    def count_products_in_use(self):
        """Count total products with users"""
        return sum(len(agent.products) for agent in self.user_agents)

    def step(self):
        """Execute one step"""
        self._steps += 1
        self.datacollector.collect(self)

        all_agents = self.user_agents + self.recycling_agents + self.remanufacturing_agents
        random.shuffle(all_agents)
        for agent in all_agents:
            agent.step()

    def run_model(self, n_steps=100):
        """Run the model"""
        for _ in range(n_steps):
            self.step()


def main():
    """Run cannibalization scenarios"""
    print("="*80)
    print("CIRCULAR ECONOMY WITH CANNIBALIZATION EFFECTS")
    print("Testing how product longevity and reconditioning quality affect sales")
    print("="*80)

    scenarios = []

    # Scenario 1: Planned Obsolescence (short product life)
    print("\n\n💰 Scenario 1: PLANNED OBSOLESCENCE")
    print("Short-lived products to maximize repeat purchases")
    print("-"*80)

    model = CircularEconomyModelWithCannibalization(
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.5,
        recycling_rate=0.7,
        product_quality=ProductQuality.LOW,  # Short-lived
        reconditioning_quality=ProductQuality.LOW  # Poor reconditioning
    )

    model.run_model(n_steps=100)

    results = {
        'scenario': 'Planned Obsolescence',
        'product_quality': 'LOW',
        'reconditioning_quality': 'LOW',
        'products_sold': model.products_sold,
        'revenue': model.total_revenue,
        'co2': model.total_co2,
        'waste': model.waste_generated,
        'remanu_rate': sum(a.products_remanufactured for a in model.remanufacturing_agents) / model.products_sold * 100 if model.products_sold > 0 else 0
    }

    print(f"Products Sold: {results['products_sold']}")
    print(f"Total Revenue: ${results['revenue']:.2f}")
    print(f"Revenue per Sale: ${results['revenue']/results['products_sold']:.2f}" if results['products_sold'] > 0 else "N/A")
    print(f"Total CO2: {results['co2']:.2f}")
    print(f"Waste Generated: {results['waste']}")
    print(f"Remanufactured Rate: {results['remanu_rate']:.1f}%")

    scenarios.append(results)

    # Scenario 2: Standard Quality
    print("\n\n⚖️  Scenario 2: STANDARD QUALITY")
    print("Medium-lived products with standard reconditioning")
    print("-"*80)

    model = CircularEconomyModelWithCannibalization(
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.5,
        recycling_rate=0.7,
        product_quality=ProductQuality.MEDIUM,
        reconditioning_quality=ProductQuality.MEDIUM
    )

    model.run_model(n_steps=100)

    results = {
        'scenario': 'Standard Quality',
        'product_quality': 'MEDIUM',
        'reconditioning_quality': 'MEDIUM',
        'products_sold': model.products_sold,
        'revenue': model.total_revenue,
        'co2': model.total_co2,
        'waste': model.waste_generated,
        'remanu_rate': sum(a.products_remanufactured for a in model.remanufacturing_agents) / model.products_sold * 100 if model.products_sold > 0 else 0
    }

    print(f"Products Sold: {results['products_sold']}")
    print(f"Total Revenue: ${results['revenue']:.2f}")
    print(f"Revenue per Sale: ${results['revenue']/results['products_sold']:.2f}" if results['products_sold'] > 0 else "N/A")
    print(f"Total CO2: {results['co2']:.2f}")
    print(f"Waste Generated: {results['waste']}")
    print(f"Remanufactured Rate: {results['remanu_rate']:.1f}%")

    scenarios.append(results)

    # Scenario 3: High Durability (CANNIBALIZATION)
    print("\n\n🌍 Scenario 3: HIGH DURABILITY")
    print("Long-lasting products with excellent reconditioning")
    print("-"*80)

    model = CircularEconomyModelWithCannibalization(
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.5,
        recycling_rate=0.7,
        product_quality=ProductQuality.HIGH,  # Long-lived
        reconditioning_quality=ProductQuality.HIGH  # Excellent reconditioning
    )

    model.run_model(n_steps=100)

    results = {
        'scenario': 'High Durability',
        'product_quality': 'HIGH',
        'reconditioning_quality': 'HIGH',
        'products_sold': model.products_sold,
        'revenue': model.total_revenue,
        'co2': model.total_co2,
        'waste': model.waste_generated,
        'remanu_rate': sum(a.products_remanufactured for a in model.remanufacturing_agents) / model.products_sold * 100 if model.products_sold > 0 else 0
    }

    print(f"Products Sold: {results['products_sold']}")
    print(f"Total Revenue: ${results['revenue']:.2f}")
    print(f"Revenue per Sale: ${results['revenue']/results['products_sold']:.2f}" if results['products_sold'] > 0 else "N/A")
    print(f"Total CO2: {results['co2']:.2f}")
    print(f"Waste Generated: {results['waste']}")
    print(f"Remanufactured Rate: {results['remanu_rate']:.1f}%")

    scenarios.append(results)

    # Scenario 4: Mixed Strategy
    print("\n\n🔄 Scenario 4: MIXED STRATEGY")
    print("Short-lived new products but excellent reconditioning")
    print("-"*80)

    model = CircularEconomyModelWithCannibalization(
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.5,
        recycling_rate=0.7,
        product_quality=ProductQuality.LOW,  # Short-lived new
        reconditioning_quality=ProductQuality.HIGH  # But great reconditioning
    )

    model.run_model(n_steps=100)

    results = {
        'scenario': 'Mixed Strategy',
        'product_quality': 'LOW',
        'reconditioning_quality': 'HIGH',
        'products_sold': model.products_sold,
        'revenue': model.total_revenue,
        'co2': model.total_co2,
        'waste': model.waste_generated,
        'remanu_rate': sum(a.products_remanufactured for a in model.remanufacturing_agents) / model.products_sold * 100 if model.products_sold > 0 else 0
    }

    print(f"Products Sold: {results['products_sold']}")
    print(f"Total Revenue: ${results['revenue']:.2f}")
    print(f"Revenue per Sale: ${results['revenue']/results['products_sold']:.2f}" if results['products_sold'] > 0 else "N/A")
    print(f"Total CO2: {results['co2']:.2f}")
    print(f"Waste Generated: {results['waste']}")
    print(f"Remanufactured Rate: {results['remanu_rate']:.1f}%")

    scenarios.append(results)

    # Comparative Analysis
    print("\n\n" + "="*80)
    print("CANNIBALIZATION ANALYSIS")
    print("="*80)

    print("\n📦 SALES VOLUME COMPARISON (Cannibalization Effect):")
    print("-"*80)
    baseline = scenarios[0]['products_sold']
    for s in scenarios:
        bar = '█' * int(s['products_sold'] / 10)
        change = ((s['products_sold'] - baseline) / baseline * 100) if baseline > 0 else 0
        print(f"{s['scenario']:<25} {s['products_sold']:>4} units {bar} ({change:+.1f}%)")

    print("\n💰 REVENUE COMPARISON:")
    print("-"*80)
    baseline_rev = scenarios[0]['revenue']
    for s in scenarios:
        bar = '█' * int(s['revenue'] / 100)
        change = ((s['revenue'] - baseline_rev) / baseline_rev * 100) if baseline_rev > 0 else 0
        print(f"{s['scenario']:<25} ${s['revenue']:>6.0f} {bar} ({change:+.1f}%)")

    print("\n🌍 CO2 EMISSIONS COMPARISON:")
    print("-"*80)
    for s in scenarios:
        bar = '█' * int(s['co2'] / 100)
        print(f"{s['scenario']:<25} {s['co2']:>7.0f} CO2 {bar}")

    print("\n🗑️  WASTE COMPARISON:")
    print("-"*80)
    for s in scenarios:
        bar = '█' * int(s['waste'] / 10)
        print(f"{s['scenario']:<25} {s['waste']:>4} units {bar}")

    print("\n\n" + "="*80)
    print("KEY FINDINGS - THE CANNIBALIZATION PARADOX")
    print("="*80)

    print(f"""
🔍 OBSERVATION:
High durability products REDUCE sales volume and revenue due to longer lifetimes.
This is the CANNIBALIZATION EFFECT.

📊 QUANTITATIVE IMPACT:
- Planned Obsolescence: {scenarios[0]['products_sold']} products sold, ${scenarios[0]['revenue']:.0f} revenue
- High Durability: {scenarios[2]['products_sold']} products sold, ${scenarios[2]['revenue']:.0f} revenue
- Sales Reduction: {((scenarios[0]['products_sold'] - scenarios[2]['products_sold']) / scenarios[0]['products_sold'] * 100):.1f}%
- Revenue Loss: ${scenarios[0]['revenue'] - scenarios[2]['revenue']:.0f}

🌍 ENVIRONMENTAL BENEFIT:
- CO2 Reduction: {scenarios[0]['co2'] - scenarios[2]['co2']:.0f} units ({((scenarios[0]['co2'] - scenarios[2]['co2']) / scenarios[0]['co2'] * 100):.1f}%)
- Waste Reduction: {scenarios[0]['waste'] - scenarios[2]['waste']} units ({((scenarios[0]['waste'] - scenarios[2]['waste']) / scenarios[0]['waste'] * 100):.1f}%)

💡 BUSINESS IMPLICATIONS:
1. Durable products reduce repeat purchases (cannibalization)
2. Short-term revenue decreases with quality improvements
3. Companies face profit vs. sustainability dilemma
4. Service models (product-as-a-service) may offset revenue loss
5. Brand reputation and long-term loyalty can compensate

🎯 STRATEGIC OPTIONS:
A) Planned Obsolescence: High revenue, high environmental impact
B) Product-as-a-Service: Charge for usage, not ownership
C) Premium Pricing: Higher margins on durable products
D) Subscription Models: Ongoing revenue from fewer sales
E) Service Revenue: Maintenance, upgrades, repairs
    """)

    return scenarios


if __name__ == "__main__":
    results = main()
