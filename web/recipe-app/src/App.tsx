import React from 'react';
import { Button, Divider, Select, List } from 'antd';
import './App.css';

type Props = {};
type State = { searchOptions: any, recipes: any, selection: string };

class App extends React.Component<Props, State> {
  constructor(props: any) {
    super(props);
    this.state = {
      searchOptions: [],
      recipes: [],
      selection: '',
    };
  }

  onSelectionChange = (value: string) => {
    this.setState({ selection: value });
  };

  onIngredientSearch = (value: string) => {
    fetch(`http://localhost:5000/ingredients?search=` + value)
      .then((response) => {
        response.json().then((json_result) => {
          const values = json_result.map((item: any) => {
            return { 'value': item, 'label': item }
          })
          this.setState({ searchOptions: values });
        }).catch(e => {
          console.log(e);
        });
      }).catch(e => {
        console.log(e);
      });
  };

  onSearchClick = (event: any) => {
    this.setState({ recipes: [] });
    fetch(`http://localhost:5000/predict`,
      {
        method: "post",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.state.selection)
      }
    ).then((response) => {
      response.json().then(json_result => {

        fetch(`http://localhost:5000/recipes?label=` + json_result["label"]).then((response) => {
          response.json().then((recipe_json) => {
            const values = recipe_json.map((item: any) => {
              return { 'title': item.name, 'subtitle': item.description, 'url': 'https://www.food.com/search/' + item.recipe_id }
            });
            this.setState({ recipes: values });
          })
        }).catch(e => { console.log(e) })
      }).catch(e => { console.log(e) })
    }).catch(e => {
      console.log(e);
    });
    console.log('search clicked', this.state.selection)
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          Recipe Finder
        </header>
        <div>
          <Divider>Search</Divider>
          <Select
            showArrow
            mode="multiple"
            onChange={this.onSelectionChange}
            onSearch={this.onIngredientSearch}
            style={{ width: '80%' }}
            options={this.state.searchOptions}
          />
          <Button type="primary" onClick={this.onSearchClick}>Search</Button>
        </div>
        <Divider>Results</Divider>
        <div>
          <List
            itemLayout="horizontal"
            style={{ width: '80%' }}
            dataSource={this.state.recipes}
            renderItem={(item: any) => (
              <List.Item>
                <List.Item.Meta
                  title={<a href={item.url}>{item.title}</a>}
                  description={item.subtitle}
                />
              </List.Item>
            )}
          />
        </div>
      </div>
    );
  }
}


export default App;
