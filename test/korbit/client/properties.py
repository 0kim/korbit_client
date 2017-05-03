from korbit.client.properties import Properties
import os

production_file = '../properties.json'
sandbox_file = '../properties_sandbox_test.json'

print( "Result of Production ")
p = Properties(production_file);
print( p.getApiUrl() )
print( p.getSiteUrl() )

print( "Result of Sandbox")
p = Properties(sandbox_file);
print( p.getApiUrl() )
print( p.getSiteUrl() )