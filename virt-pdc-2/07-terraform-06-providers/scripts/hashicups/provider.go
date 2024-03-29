  GNU nano 4.8                                      provider.go
package hashicups

import (
        "github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
)

// Provider -
func Provider() *schema.Provider {
        return &schema.Provider{
                ResourcesMap: map[string]*schema.Resource{},
                DataSourcesMap: map[string]*schema.Resource{
                        "hashicups_coffees": dataSourceCoffees(),
                },
        }
}


