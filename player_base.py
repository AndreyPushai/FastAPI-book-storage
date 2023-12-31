from typing import Literal, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import HTTPException
from utils.time_generator import ns_timestamp


facility_data = {
    1: {"price": 100, "construction_time": 60},
    2: {"price": 200, "construction_time": 180},
    3: {"price": 400, "construction_time": 1800},
    4: {"price": 600, "construction_time": 2400},
    5: {"price": 1200, "construction_time": 6400}
}


def set_facility_data():
    pass


class Facility(BaseModel):
    type: Literal["MoneyFacility", "CrystalsFacility"]
    level: int = Field(default=1, ge=1, le=5)
    price: int
    construction_time: int


    def get_next_level_requirements(self):
        next_level = self.level + 1
        print(self.get_facility_data(next_level))


    def upgrade(self):
        # check requirements:
        # max level
        # price 
        self.level += 1
        self.price = facility_data.get(self.level).get("price")
        self.construction_time = facility_data.get(self.level).get("construction_time")
        # self.construction_end_time

        # price = MoneySpawnFacility().price
        # if self.money < price:
        #     raise HTTPException(status_code=422, detail=f"Not enough money!")

        # self.set_money(self.money - price)
        # self.facilities.append(MoneySpawnFacility())



    @classmethod
    def get_facility_data(cls, level: int) -> Dict:
        return facility_data.get(level)


    # @property
    # def facility_price(self) -> int:
    #     return self.get_facility_data(self.level).get("price", 0)


    # @property
    # def construction_time(self) -> int:
    #     return self.get_facility_data(self.level).get("construction_time", 0)


# spawn time = 1h
money_facility_stats = {
    1: {"capacity": 1000, "production_quantity": 200, "build_price": 150, "build_time": 10},
    2: {"capacity": 2000, "production_quantity": 400, "build_price": 300, "build_time": 60},
    3: {"capacity": 5000, "production_quantity": 1000, "build_price": 600, "build_time": 240},
    4: {"capacity": 10000, "production_quantity": 2000, "build_price": 1500, "build_time": 600},
    5: {"capacity": 20000, "production_quantity": 4000, "build_price": 3000, "build_time": 2400},
}


class MoneySpawnFacility(BaseModel):
    id: int = Field(default_factory=ns_timestamp)
    level: int = Field(default=1, ge=1, le=5)
    type: str = Field(default="MoneyFacility")
    capacity: int
    production_quantity: int
    spawn_time: int = Field(default=3600)
    money: int = Field(default=0)


    def produce(self):
        # Check if the money capacity reached max
        if (self.money + self.production_quantity) > self.capacity:
            raise HTTPException(status_code=400, detail=f"Max capacity reached.")

        self.money += self.production_quantity


    def collect(self):
        # Add capacity to user money
        # user_money = user_money + self.money
        # Clear money
        self.money = 0
        # Start producing
        # self.produce()


    def get_next_level_requirements(self):
        next_level = self.level + 1
        return self.get_money_facility_stats(next_level)


    def upgrade(self):
        # check requirements:
        # max level
        # price 
        self.level += 1
        self.capacity = money_facility_stats.get(self.level).get("capacity")
        self.production_quantity = money_facility_stats.get(self.level).get("production_quantity")


    @classmethod
    def get_money_facility_stats(cls, level: int) -> Dict:
        return money_facility_stats.get(level)


class CrystalsSpawnFacility(Facility):
    type: str = Field(default="CrystalsFacility")
    price: int = Field(default=10)
    construction_time: int = Field(default=60)
    level: int = Field(default=1, ge=1, le=5)
    money: int = Field(default=0)


class PlayerBase(BaseModel):
    # max per level?
    money: int = Field(default=0)
    crystals: int = Field(default=0)
    facilities: list = Field(default=[])


    def set_money(self, value: int):
        self.money = value


    def set_crystals(self, value: int):
        self.crystals = value


    def build_money_facility(self):
        stats = money_facility_stats.get(1)
        build_price = stats.get("build_price")

        if self.money < build_price:
            raise Exception(f"Requirement not met: {build_price}. Not enough money!")
            raise HTTPException(status_code=422, detail=f"Requirement not met: {build_price}. Not enough money!")

        self.set_money(self.money - build_price)
        self.facilities.append(MoneySpawnFacility(
            capacity = stats.get("capacity"),
            production_quantity = stats.get("production_quantity")
        ))


    def build_crystals_facility(self):
        price = MoneySpawnFacility().price
        if self.money < price:
            raise HTTPException(status_code=422, detail=f"Not enough money!")

        self.set_money(self.money - price)
        self.facilities.append(MoneySpawnFacility())


    def get_facility(self, id: int):
        try:
            facility = next(facility for facility in self.facilities if facility.id == id)
        except StopIteration:
            raise HTTPException(status_code=422, detail=f"Facility {id=} not found.")
        else:
            return facility


    def collect_money(self):
        money_facilities = [facility for facility in self.facilities if facility.type == "MoneyFacility"]
        for facility in money_facilities:
            self.money += facility.money
            facility.money = 0


    def upgrade_money_facility(self, id: int):
        facility: MoneySpawnFacility = self.get_facility(id)
        build_price = facility.get_next_level_requirements().get("build_price")

        if self.money < build_price:
            raise Exception(f"Requirement not met: {build_price}. Not enough money!")
            raise HTTPException(status_code=422, detail=f"Requirement not met: {build_price}. Not enough money!")

        self.set_money(self.money - build_price)
        facility.upgrade()

    # forces
    # defence
