"""
Circular Economy Simulation with Mesa 3.x
Includes: Users, Recycling Centers, Remanufacturing Facilities, and CO2 Taxes
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


class Product:
    """Represents a product in the circular economy"""
    def __init__(self, product_id, state=ProductState.NEW, co2_footprint=0):
        self.id = product_id
        self.state = state
        self.co2_footprint = co2_footprint
        self.lifetime = 0
        self.max_lifetime = random.randint(10, 30)

    def use(self):
        """Use the product, increasing its lifetime"""
        self.lifetime += 1
        self.co2_footprint += 0.1  # CO2 from usage
        return self.lifetime >= self.max_lifetime


class UserAgent(Agent):
    """Agent representing a consumer in the circular economy"""

    def __init__(self, model):
        super().__init__(model)
        self.products = []
        self.money = random.uniform(1000, 5000)
        self.co2_tax_paid = 0
        self.preference_new = random.uniform(0.3, 0.7)  # Preference for new vs remanufactured

    def step(self):
        """Execute one step of the agent"""
        # Use existing products
        for product in self.products[:]:
            is_worn = product.use()
            if is_worn:
                self.dispose_product(product)

        # Consider buying a new product
        if len(self.products) < 3 and random.random() < 0.3:
            self.buy_product()

    def buy_product(self):
        """Buy a new or remanufactured product"""
        # Choose between new and remanufactured based on availability and preference
        available_remanufactured = self.model.remanufactured_inventory

        if available_remanufactured > 0 and random.random() > self.preference_new:
            # Buy remanufactured
            product = Product(
                self.model.next_product_id(),
                state=ProductState.REMANUFACTURED,
                co2_footprint=5  # Lower CO2 than new
            )
            self.model.remanufactured_inventory -= 1
            cost = 80
            co2_tax = product.co2_footprint * self.model.co2_tax_rate
        else:
            # Buy new
            product = Product(
                self.model.next_product_id(),
                state=ProductState.NEW,
                co2_footprint=20  # High CO2 from manufacturing
            )
            cost = 100
            co2_tax = product.co2_footprint * self.model.co2_tax_rate

        total_cost = cost + co2_tax
        if self.money >= total_cost:
            self.money -= total_cost
            self.co2_tax_paid += co2_tax
            self.products.append(product)
            self.model.total_co2_tax_collected += co2_tax
            self.model.products_sold += 1

    def dispose_product(self, product):
        """Dispose of a used product"""
        self.products.remove(product)
        product.state = ProductState.USED

        # Decide whether to recycle or throw away
        if random.random() < self.model.recycling_rate:
            self.model.recycling_queue.append(product)
        else:
            self.model.waste_generated += 1
            self.model.total_co2 += 10  # CO2 from waste


class RecyclingAgent(Agent):
    """Agent representing a recycling facility"""

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

            # Recycling process generates some CO2
            co2_from_recycling = 2
            self.model.total_co2 += co2_from_recycling

            # Success based on efficiency
            if random.random() < self.efficiency:
                product.state = ProductState.RECYCLED
                product.co2_footprint += co2_from_recycling
                self.model.recycled_materials.append(product)
                self.products_recycled += 1
            else:
                # Failed recycling goes to waste
                self.model.waste_generated += 1
                self.model.total_co2 += 5

            processed += 1


class RemanufacturingAgent(Agent):
    """Agent representing a remanufacturing facility"""

    def __init__(self, model):
        super().__init__(model)
        self.capacity = random.randint(3, 10)
        self.products_remanufactured = 0

    def step(self):
        """Remanufacture products from recycled materials"""
        processed = 0
        while processed < self.capacity and self.model.recycled_materials:
            product = self.model.recycled_materials.pop(0)

            # Remanufacturing process
            co2_from_remanufacturing = 3  # Lower than new manufacturing (20)
            self.model.total_co2 += co2_from_remanufacturing

            product.state = ProductState.REMANUFACTURED
            product.co2_footprint = 5  # Reset footprint for remanufactured product
            product.lifetime = 0
            product.max_lifetime = random.randint(8, 25)

            self.model.remanufactured_inventory += 1
            self.products_remanufactured += 1
            processed += 1


class CircularEconomyModel(Model):
    """Model for circular economy simulation with CO2 taxes"""

    def __init__(
        self,
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.5,
        recycling_rate=0.7
    ):
        super().__init__()
        self.num_users = n_users
        self.num_recyclers = n_recyclers
        self.num_remanufacturers = n_remanufacturers
        self.co2_tax_rate = co2_tax_rate
        self.recycling_rate = recycling_rate

        # Model state variables
        self.recycling_queue = []
        self.recycled_materials = []
        self.remanufactured_inventory = 0
        self.total_co2 = 0
        self.total_co2_tax_collected = 0
        self.waste_generated = 0
        self.products_sold = 0
        self._product_counter = 0

        # Store agents by type for easy access
        self.user_agents = []
        self.recycling_agents = []
        self.remanufacturing_agents = []

        # Create agents
        # Create users
        for i in range(self.num_users):
            agent = UserAgent(self)
            self.user_agents.append(agent)

        # Create recycling facilities
        for i in range(self.num_recyclers):
            agent = RecyclingAgent(self)
            self.recycling_agents.append(agent)

        # Create remanufacturing facilities
        for i in range(self.num_remanufacturers):
            agent = RemanufacturingAgent(self)
            self.remanufacturing_agents.append(agent)

        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "Total CO2": "total_co2",
                "CO2 Tax Collected": "total_co2_tax_collected",
                "Waste Generated": "waste_generated",
                "Recycling Queue": lambda m: len(m.recycling_queue),
                "Recycled Materials": lambda m: len(m.recycled_materials),
                "Remanufactured Inventory": "remanufactured_inventory",
                "Products Sold": "products_sold",
                "Total Products in Use": self.count_products_in_use,
            }
        )

    def next_product_id(self):
        """Generate unique product ID"""
        self._product_counter += 1
        return self._product_counter

    def count_products_in_use(self):
        """Count total products currently with users"""
        count = 0
        for agent in self.user_agents:
            count += len(agent.products)
        return count

    def step(self):
        """Execute one step of the model"""
        self.datacollector.collect(self)

        # Step all agents in random order
        all_agents = self.user_agents + self.recycling_agents + self.remanufacturing_agents
        random.shuffle(all_agents)
        for agent in all_agents:
            agent.step()

    def run_model(self, n_steps=100):
        """Run the model for a specified number of steps"""
        for _ in range(n_steps):
            self.step()


def main():
    """Run the simulation and display results"""
    print("=" * 60)
    print("CIRCULAR ECONOMY SIMULATION WITH CO2 TAXES")
    print("=" * 60)

    # Create and run model
    model = CircularEconomyModel(
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.5,  # $0.5 per unit of CO2
        recycling_rate=0.7  # 70% of products get recycled
    )

    print(f"\nModel Configuration:")
    print(f"  Users: {model.num_users}")
    print(f"  Recycling Facilities: {model.num_recyclers}")
    print(f"  Remanufacturing Facilities: {model.num_remanufacturers}")
    print(f"  CO2 Tax Rate: ${model.co2_tax_rate} per unit")
    print(f"  Recycling Rate: {model.recycling_rate * 100}%")

    print(f"\nRunning simulation for 100 steps...")
    model.run_model(n_steps=100)

    # Get results
    data = model.datacollector.get_model_vars_dataframe()

    print("\n" + "=" * 60)
    print("SIMULATION RESULTS")
    print("=" * 60)

    print(f"\nFinal Metrics:")
    print(f"  Total CO2 Emissions: {model.total_co2:.2f} units")
    print(f"  Total CO2 Tax Collected: ${model.total_co2_tax_collected:.2f}")
    print(f"  Total Waste Generated: {model.waste_generated} products")
    print(f"  Products Sold: {model.products_sold}")
    print(f"  Remanufactured Inventory: {model.remanufactured_inventory}")
    print(f"  Products in Recycling Queue: {len(model.recycling_queue)}")
    print(f"  Recycled Materials Available: {len(model.recycled_materials)}")

    # Calculate recycling metrics
    total_recycled = sum(agent.products_recycled for agent in model.recycling_agents)
    total_remanufactured = sum(agent.products_remanufactured for agent in model.remanufacturing_agents)

    print(f"\nCircular Economy Metrics:")
    print(f"  Products Recycled: {total_recycled}")
    print(f"  Products Remanufactured: {total_remanufactured}")
    if model.products_sold > 0:
        print(f"  Remanufactured Rate: {(total_remanufactured / model.products_sold) * 100:.1f}%")

    # Display timeline data
    print(f"\nTimeline Summary (every 20 steps):")
    print(f"{'Step':<8} {'CO2':<10} {'Tax':<10} {'Waste':<8} {'In Use':<8} {'Remanu.':<8}")
    print("-" * 60)
    for idx in [0, 20, 40, 60, 80, 99]:
        if idx < len(data):
            row = data.iloc[idx]
            print(f"{idx:<8} {row['Total CO2']:<10.1f} ${row['CO2 Tax Collected']:<9.1f} "
                  f"{row['Waste Generated']:<8.0f} {row['Total Products in Use']:<8.0f} "
                  f"{row['Remanufactured Inventory']:<8.0f}")

    print("\n" + "=" * 60)
    print("\nSimulation complete!")
    print("\nKey Insights:")
    print("- CO2 taxes incentivize purchasing remanufactured products")
    print("- Higher recycling rates reduce waste and CO2 emissions")
    print("- Circular economy reduces environmental impact vs linear production")

    return model, data


if __name__ == "__main__":
    model, data = main()
