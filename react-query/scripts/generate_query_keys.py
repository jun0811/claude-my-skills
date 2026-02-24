#!/usr/bin/env python3
"""
Generate React Query Key Factory files from entity names.
Creates TypeScript files with hierarchical query key structures.

Usage:
    python generate_query_keys.py user post comment
    
This will create:
    - userKeys.ts
    - postKeys.ts
    - commentKeys.ts

Each file contains a type-safe query key factory with:
    - all: base key for the entity
    - lists: key for list queries
    - list: key for filtered list queries
    - details: key for detail queries
    - detail: key for specific item queries
"""

import sys
from pathlib import Path


def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_pascal_case(snake_str: str) -> str:
    """Convert snake_case to PascalCase."""
    return ''.join(x.title() for x in snake_str.split('_'))


def generate_query_key_factory(entity_name: str) -> str:
    """Generate query key factory code for an entity."""
    camel_name = to_camel_case(entity_name)
    pascal_name = to_pascal_case(entity_name)
    plural_name = f"{entity_name}s" if not entity_name.endswith('s') else entity_name
    
    template = f'''/**
 * Query key factory for {pascal_name} queries
 * 
 * Hierarchical structure allows efficient cache invalidation:
 * - {camel_name}Keys.all → invalidates all {entity_name}-related queries
 * - {camel_name}Keys.lists() → invalidates all list queries
 * - {camel_name}Keys.details() → invalidates all detail queries
 * 
 * @example
 * // Invalidate all {entity_name} queries
 * queryClient.invalidateQueries({{ queryKey: {camel_name}Keys.all }});
 * 
 * @example
 * // Invalidate specific {entity_name} detail
 * queryClient.invalidateQueries({{ queryKey: {camel_name}Keys.detail(id) }});
 */
export const {camel_name}Keys = {{
  all: ['{plural_name}'] as const,
  lists: () => [...{camel_name}Keys.all, 'list'] as const,
  list: (filters?: {pascal_name}Filters) => [...{camel_name}Keys.lists(), {{ filters }}] as const,
  details: () => [...{camel_name}Keys.all, 'detail'] as const,
  detail: (id: number) => [...{camel_name}Keys.details(), id] as const,
}} as const;

/**
 * Type alias for all possible {pascal_name} query keys
 */
export type {pascal_name}Keys = ReturnType<typeof {camel_name}Keys[keyof typeof {camel_name}Keys]>;

/**
 * Filter options for {entity_name} list queries
 * 
 * @example
 * const {{ data }} = useQuery({{
 *   queryKey: {camel_name}Keys.list({{ status: 'active' }}),
 *   queryFn: () => fetch{pascal_name}s({{ status: 'active' }})
 * }});
 */
export interface {pascal_name}Filters {{
  // TODO: Add filter fields
  // status?: 'active' | 'inactive';
  // search?: string;
  // sortBy?: string;
}}
'''
    return template


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_query_keys.py <entity_name> [entity_name2] ...")
        print("Example: python generate_query_keys.py user post comment")
        sys.exit(1)
    
    entity_names = sys.argv[1:]
    output_dir = Path.cwd() / "src" / "queries" / "keys"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    created_files = []
    
    for entity_name in entity_names:
        entity_name = entity_name.lower().strip()
        camel_name = to_camel_case(entity_name)
        filename = f"{camel_name}Keys.ts"
        filepath = output_dir / filename
        
        content = generate_query_key_factory(entity_name)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        created_files.append(filepath)
        print(f"✅ Created: {filepath}")
    
    # Generate index file
    index_content = "// Auto-generated query key exports\n\n"
    for entity_name in entity_names:
        camel_name = to_camel_case(entity_name)
        index_content += f"export * from './{camel_name}Keys';\n"
    
    index_path = output_dir / "index.ts"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Created: {index_path}")
    print(f"\n🎉 Successfully generated {len(created_files)} query key factories!")
    print(f"\nNext steps:")
    print(f"1. Update {to_pascal_case(entity_names[0])}Filters interface with your actual filter fields")
    print(f"2. Import and use: import {{ {to_camel_case(entity_names[0])}Keys }} from '@/queries/keys'")


if __name__ == "__main__":
    main()
