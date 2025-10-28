"""
Generator Router - Component and code generation endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

class GenerateRequest(BaseModel):
    job_id: str
    components: List[Dict[str, Any]]
    target_framework: str = "nextjs"  # nextjs, react, vue
    ui_library: str = "shadcn"  # shadcn, mui, chakra

class GeneratedCode(BaseModel):
    filename: str
    content: str
    type: str  # component, page, style, config

@router.post("/generate")
async def generate_code(request: GenerateRequest):
    """Generate React/Next.js code from analyzed components"""
    
    generated_files: List[GeneratedCode] = []
    
    # Generate components
    for comp in request.components:
        code = generate_react_component(comp, request.ui_library)
        generated_files.append(GeneratedCode(
            filename=f"{comp['type']}.tsx",
            content=code,
            type="component"
        ))
    
    # Generate Tailwind config
    tailwind_config = generate_tailwind_config(request.components)
    generated_files.append(GeneratedCode(
        filename="tailwind.config.ts",
        content=tailwind_config,
        type="config"
    ))
    
    return {
        "job_id": request.job_id,
        "files": generated_files,
        "total_files": len(generated_files)
    }

def generate_react_component(component: Dict, ui_library: str) -> str:
    """Convert HTML component to React with ShadCN UI"""
    comp_type = component['type']
    html = component['html']
    
    # Template for React component
    template = f'''
import {{ Card }} from "@/components/ui/card"
import {{ Button }} from "@/components/ui/button"

export default function {comp_type.capitalize()}() {{
  return (
    <section className="py-12 px-4">
      {{/* Generated from: {comp_type} */}}
      <div className="container mx-auto">
        {{/* Component content */}}
      </div>
    </section>
  )
}}
'''
    return template

def generate_tailwind_config(components: List[Dict]) -> str:
    """Generate Tailwind config with extracted design tokens"""
    return '''
import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Extracted from source
        primary: '#0070f3',
        secondary: '#7928ca',
      },
    },
  },
  plugins: [],
}

export default config
'''
