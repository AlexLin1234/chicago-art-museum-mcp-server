# Usage Examples

This document provides detailed examples of how to use the Art Institute of Chicago MCP server with Claude.

## Basic Searches

### Search for Artworks by Artist

**Prompt:**
```
Search for artworks by Vincent van Gogh in the Art Institute of Chicago collection.
```

**What Claude will do:**
- Use the `search_artworks` tool with query "Vincent van Gogh"
- Return artwork details including titles, dates, descriptions, and image URLs

---

### Search for Artworks by Style or Movement

**Prompt:**
```
Find impressionist paintings in the Art Institute of Chicago.
```

**What Claude will do:**
- Search for "impressionist" in the artwork database
- Display matching artworks with full metadata

---

### Get Specific Artwork Details

**Prompt:**
```
Tell me about artwork ID 27992 from the Art Institute of Chicago.
```

**What Claude will do:**
- Use `get_artwork` tool with the specified ID
- Return comprehensive information including:
  - Title, artist, and dates
  - Medium and dimensions
  - Provenance and exhibition history
  - High-resolution image links

---

## Advanced Searches

### Search by Time Period

**Prompt:**
```
Show me Japanese woodblock prints from the 18th century.
```

**What Claude will do:**
- Search with relevant terms
- Filter and present artworks matching the criteria

---

### Search by Medium or Material

**Prompt:**
```
Find oil paintings on canvas by American artists.
```

**What Claude will do:**
- Search using medium and artist origin filters
- Display matching results

---

## Artist Information

### Artist Biography

**Prompt:**
```
Tell me about the artist Georgia O'Keeffe using the Art Institute database.
```

**What Claude will do:**
- Use `search_agents` to find the artist
- Display biographical information including birth/death dates and description
- Optionally search for their artworks in the collection

---

### Compare Artists

**Prompt:**
```
Compare the works of Monet and Renoir in the Art Institute collection.
```

**What Claude will do:**
- Search for artworks by both artists
- Present side-by-side comparisons
- Discuss similarities and differences

---

## Exhibition Information

### Current Exhibitions

**Prompt:**
```
What are the current exhibitions at the Art Institute of Chicago?
```

**What Claude will do:**
- Use `search_exhibitions` or list exhibitions
- Filter for current/open status
- Display exhibition details and dates

---

### Historical Exhibitions

**Prompt:**
```
Find past exhibitions about surrealism at the Art Institute.
```

**What Claude will do:**
- Search exhibitions with "surrealism" query
- Display historical exhibition information

---

## Gallery and Location

### Find Gallery Locations

**Prompt:**
```
Where can I find the European painting galleries?
```

**What Claude will do:**
- Use `list_galleries` to browse galleries
- Filter for relevant galleries
- Provide location information (floor, room number)

---

### Check Gallery Status

**Prompt:**
```
Are there any closed galleries right now?
```

**What Claude will do:**
- List galleries and check their status
- Report which galleries are temporarily closed

---

## Complex Queries

### Thematic Exploration

**Prompt:**
```
Show me artworks in the Art Institute's collection that feature water or the ocean.
```

**What Claude will do:**
- Search with relevant keywords
- Present diverse artworks matching the theme
- Provide context and descriptions

---

### Cultural Context

**Prompt:**
```
Find ancient Egyptian artifacts and tell me about them.
```

**What Claude will do:**
- Search for Egyptian artworks
- Provide historical context
- Explain cultural significance

---

### Cross-Reference Artworks and Artists

**Prompt:**
```
Find artworks from the Renaissance period and tell me about the artists who created them.
```

**What Claude will do:**
- Search for Renaissance artworks
- Use agent search to get artist biographies
- Provide comprehensive information about both

---

## Research and Analysis

### Artwork Analysis

**Prompt:**
```
Analyze the composition and symbolism in Grant Wood's "American Gothic" if it's in the collection.
```

**What Claude will do:**
- Search for the artwork
- Provide detailed information from the museum's database
- Add contextual analysis based on the metadata

---

### Collection Statistics

**Prompt:**
```
How many artworks by Spanish artists are in the collection?
```

**What Claude will do:**
- Search with relevant parameters
- Report pagination data showing total results
- Provide representative examples

---

## Educational Use Cases

### Art History Research

**Prompt:**
```
I'm writing a paper on Post-Impressionism. Find relevant artworks and information.
```

**What Claude will do:**
- Search for Post-Impressionist artworks
- Provide detailed artwork information
- Suggest related artists and movements

---

### Exhibition Planning

**Prompt:**
```
Help me plan a visit to see French Impressionist paintings.
```

**What Claude will do:**
- Search for French Impressionist works
- Provide gallery locations
- Suggest must-see pieces

---

## Pagination Examples

### Browse Multiple Pages

**Prompt:**
```
Show me the first 20 artworks by Pablo Picasso, then show me the next 20.
```

**First request:**
```json
{
  "query": "Pablo Picasso",
  "limit": 20,
  "page": 1
}
```

**Second request:**
```json
{
  "query": "Pablo Picasso",
  "limit": 20,
  "page": 2
}
```

---

## Field Filtering

### Get Specific Fields Only

**Prompt:**
```
Search for Monet artworks but only show me the title, artist, and image.
```

**What Claude will do:**
- Use the `fields` parameter to request only specific data
- Return streamlined results with just the requested information

---

## Tips for Best Results

1. **Be Specific**: More specific queries yield better results
   - Good: "French impressionist landscapes"
   - Less good: "paintings"

2. **Use Artwork IDs**: When you know the ID, direct retrieval is most efficient
   - "Get artwork 27992" is faster than searching

3. **Combine Searches**: Claude can combine multiple tool calls
   - "Find artworks by Monet and tell me about him as an artist"

4. **Explore Relationships**: Use the data to discover connections
   - "Show me artworks from the same exhibition as artwork ID 12345"

5. **Leverage Pagination**: For comprehensive research
   - "Show me all available information about Japanese prints"

---

## Error Handling

If a search returns no results:
```
Search for "xyz123" returned no results.
```

Try:
- Broadening your search terms
- Checking spelling
- Using alternative terminology
- Searching by category instead of specific terms

---

## Advanced Features

### IIIF Image URLs

All artworks with images include IIIF URLs, allowing you to:
- Request specific image sizes
- Crop or rotate images
- Access maximum resolution versions

Example IIIF URL format:
```
https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg
```

### Cross-Collection Searching

Use `search_all` for broad discovery:
```
Search across all Art Institute collections for "Japanese art"
```

This will return artworks, exhibitions, agents, and other resources.
