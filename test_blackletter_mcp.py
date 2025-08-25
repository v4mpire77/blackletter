import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

async def test_blackletter_mcp():
    """Test the blackletter MCP server connection and functionality."""
    print("🚀 Testing Blackletter MCP Server Setup...")
    
    # Load environment variables
    load_dotenv()
    
    client = None
    try:
        # Create MCPClient from config file
        print("📋 Loading MCP configuration...")
        client = MCPClient.from_config_file("blackletter_mcp_config.json")
        
        # Create sessions to test connection
        print("🔗 Creating MCP sessions...")
        await client.create_all_sessions()
        
        # List available tools
        print("🛠️  Checking available tools...")
        session = client.get_session("blackletter_docs")
        tools = await session.list_tools()
        
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
        # List available resources
        print("\n📚 Checking available resources...")
        resources = await session.list_resources()
        print(f"✅ Found {len(resources)} resources:")
        for resource in resources:
            print(f"   - {resource.name}: {resource.description}")
        
        # Test with LLM if OpenAI API key is available
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            print("\n🤖 Testing with OpenAI LLM...")
            llm = ChatOpenAI(model="gpt-4o-mini")
            
            # Create agent with the client
            agent = MCPAgent(llm=llm, client=client, max_steps=10)
            
            # Test query
            result = await agent.run(
                "What is the blackletter project about? Give me a brief overview.",
                max_steps=5
            )
            print(f"🎯 Agent Response: {result}")
        else:
            print("\n⚠️  No OpenAI API key found. Skipping LLM test.")
            print("   Set OPENAI_API_KEY environment variable to test with LLM.")
        
        print("\n✅ MCP Server setup successful!")
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        try:
            if client and hasattr(client, 'sessions') and client.sessions:
                print("🧹 Cleaning up sessions...")
                await client.close_all_sessions()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_blackletter_mcp())
