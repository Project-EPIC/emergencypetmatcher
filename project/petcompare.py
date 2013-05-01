
from home.models import PetReport

'''this function compares 6 attributes of both pets and returns the number of matching attributes.
the attributes compared are: age, sex, size,spayed_or_neutered,pet_name and breed'''
def compare_pets(pet1,pet2):
	matching_attrs = 0
	if pet1.sex == pet2.sex:
		matching_attrs += 1
	if pet1.size == pet2.size:
		matching_attrs += 1
	if pet1.spayed_or_neutered == pet2.spayed_or_neutered:
		matching_attrs += 1
	if pet1.pet_name.lower() == pet2.pet_name.lower():
		matching_attrs += 1
	if pet1.breed.lower() == pet2.breed.lower():
		matching_attrs += 1
	if pet1.age == pet2.age:
		matching_attrs += 1

	return 'match'+str(matching_attrs)